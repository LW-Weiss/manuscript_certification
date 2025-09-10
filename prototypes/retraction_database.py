"""
Extracts and updates a duckdb database based on the data From Retraction Watch:
https://gitlab.com/crossref/retraction-watch-data/-/blob/main/retraction_watch.csv
"""
import duckdb
import pandas as pd
import numpy as np
import requests
from pathlib import Path
from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel, Field


class RetractionRecord(BaseModel):
    """Pydantic model representing a retraction record from Retraction Watch CSV."""
    record_id: Optional[int] = Field(None, alias="Record ID")
    title: Optional[str] = Field(None, alias="Title")
    subject: Optional[str] = Field(None, alias="Subject")
    institution: Optional[str] = Field(None, alias="Institution")
    journal: Optional[str] = Field(None, alias="Journal")
    publisher: Optional[str] = Field(None, alias="Publisher")
    country: Optional[str] = Field(None, alias="Country")
    author: Optional[str] = Field(None, alias="Author")
    article_type: Optional[str] = Field(None, alias="ArticleType")
    retraction_date: Optional[str] = Field(None, alias="RetractionDate")
    retraction_doi: Optional[str] = Field(None, alias="RetractionDOI")
    retraction_pmid: Optional[str] = Field(None, alias="RetractionPMID")
    retraction_nature: Optional[str] = Field(None, alias="RetractionNature")
    reason: Optional[str] = Field(None, alias="Reason")
    paywalled: Optional[str] = Field(None, alias="Paywalled")
    original_paper_date: Optional[str] = Field(None, alias="OriginalPaperDate")
    original_paper_doi: Optional[str] = Field(None, alias="OriginalPaperDOI")
    original_paper_pmid: Optional[str] = Field(None, alias="OriginalPaperPMID")
    original_paper_pmcid: Optional[str] = Field(None, alias="OriginalPaperPMCID")
    notes: Optional[str] = Field(None, alias="Notes")
    urls: Optional[str] = Field(None, alias="URLs")

    class Config:
        validate_by_name = True
        ser_json_inf_nan="null"


class RetractionDatabase:
    """Class to manage retraction data in DuckDB."""
    
    def __init__(self, db_path: str = "retraction_watch.duckdb"):
        self.db_path = Path(db_path)
        self.conn = None
    
    def connect(self):
        """Connect to DuckDB database."""
        self.conn = duckdb.connect(str(self.db_path))
        self._create_table_if_not_exists()
    
    def disconnect(self):
        """Disconnect from DuckDB database."""
        if self.conn:
            self.conn.close()
            self.conn = None
    
    def head(self, n: int = 5) -> pd.DataFrame:
        """Return the first n records from the retractions table."""
        if self.conn is None:
            self.connect()
        df = self.conn.execute(f"SELECT * FROM retractions LIMIT {n};").df()
        self.disconnect()
        return df
    
    
    def query(self, sql: str) -> pd.DataFrame:
        """Execute a SQL query and return the results as a DataFrame."""
        if self.conn is None:
            self.connect()
        df = self.conn.execute(sql).df()
        self.disconnect()
        return df
    
    def _create_table_if_not_exists(self):
        """Create the retractions table if it doesn't exist."""
        create_table_sql = """
        CREATE TABLE IF NOT EXISTS retractions (
            record_id INTEGER,
            title TEXT,
            subject TEXT,
            institution TEXT,
            journal TEXT,
            publisher TEXT,
            country TEXT,
            author TEXT,
            article_type TEXT,
            retraction_date TEXT,
            retraction_doi TEXT,
            retraction_pmid TEXT,
            retraction_nature TEXT,
            reason TEXT,
            paywalled TEXT,
            original_paper_date TEXT,
            original_paper_doi TEXT,
            original_paper_pmid TEXT,
            original_paper_pmcid TEXT,
            notes TEXT,
            urls TEXT,
            last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """
        self.conn.execute(create_table_sql)
    
    def get_last_update(self) -> Optional[datetime]:
        """Get the timestamp of the last database update."""
        try:
            result = self.conn.execute(
                "SELECT MAX(last_updated) FROM retractions"
            ).fetchone()
            return result[0] if result and result[0] else None
        except:
            return None
    
    def import_csv(self, csv_path: Optional[str] = None, force_update: bool = False):
        """Import data from CSV file to DuckDB."""
        default_url = "https://gitlab.com/crossref/retraction-watch-data/-/raw/main/retraction_watch.csv"
        
        if csv_path is None:
            # Download from default URL
            print(f"Downloading data from {default_url}...")
            pd.read_csv(default_url).to_csv("temp_retraction_watch.csv.gz", index=False)
            csv_file = Path("temp_retraction_watch.csv.gz")
            csv_path = str(csv_file)
        else:
            csv_file = Path(csv_path)
            if not csv_file.exists():
                raise FileNotFoundError(f"CSV file not found: {csv_path}")
        
        # Check if update is needed
        csv_modified = datetime.fromtimestamp(csv_file.stat().st_mtime)
        last_update = self.get_last_update()
        
        if not force_update and last_update and csv_modified <= last_update:
            print("Database is up to date. No import needed.")
            return
        
        print(f"Importing data from {csv_path}...")
        
        # Read CSV with pandas
        df = pd.read_csv(csv_path)
        df.replace({pd.NA: None, np.nan: None}, inplace=True)
        
        # Clear existing data
        self.conn.execute("DELETE FROM retractions")
        
        # Insert new data
        insert_sql = """
        INSERT INTO retractions (
            record_id, title, subject, institution, journal, publisher,
            country, author, article_type, retraction_date, retraction_doi,
            retraction_pmid, retraction_nature, reason, paywalled,
            original_paper_date, original_paper_doi, original_paper_pmid,
            original_paper_pmcid, notes, urls, last_updated
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
        """
        
        # Convert DataFrame to list of tuples for insertion
        data_tuples = []
        for _, row in df.iterrows():
            record = RetractionRecord(**row.to_dict())
            data_tuples.append((
                record.record_id, record.title, record.subject, record.institution,
                record.journal, record.publisher, record.country, record.author,
                record.article_type, record.retraction_date, record.retraction_doi,
                record.retraction_pmid, record.retraction_nature, record.reason,
                record.paywalled, record.original_paper_date, record.original_paper_doi,
                record.original_paper_pmid, record.original_paper_pmcid, record.notes,
                record.urls
            ))
        
        self.conn.executemany(insert_sql, data_tuples)
        print(f"Successfully imported {len(data_tuples)} records.")
        
        # Clean up temporary file if we downloaded it
        if csv_path is None and csv_file.name == "temp_retraction_watch.csv.gz":
            csv_file.unlink()
    
    def get_record_count(self) -> int:
        """Get the total number of records in the database."""
        result = self.conn.execute("SELECT COUNT(*) FROM retractions").fetchone()
        return result[0] if result else 0
    
    def search_by_journal(self, journal_name: str) -> List[dict]:
        """Search retractions by journal name."""
        result = self.conn.execute(
            "SELECT * FROM retractions WHERE journal ILIKE ?",
            [f"%{journal_name}%"]
        ).fetchall()
        
        columns = [desc[0] for desc in self.conn.description]
        return [dict(zip(columns, row)) for row in result]
    
    def __enter__(self):
        self.connect()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.disconnect()


if __name__ == "__main__":
    # Example usage
    with RetractionDatabase() as db:
        # Import CSV data (replace with actual path)
        db.import_csv()
        
        print(f"Total records: {db.get_record_count()}")
        print(f"Last update: {db.get_last_update()}")
