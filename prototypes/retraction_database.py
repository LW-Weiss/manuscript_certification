"""
Extracts and updates a duckdb database based on the data From Retraction Watch:
https://gitlab.com/crossref/retraction-watch-data/-/blob/main/retraction_watch.csv
"""
import duckdb
import numpy as np
from pathlib import Path
from typing import Optional, List
from datetime import datetime
        ser_json_inf_nan="null"


class RetractionDatabase:
    """Class to manage retraction data in DuckDB."""
    
    def __init__(self, db_path: str = "retraction_watch.duckdb"):
        self.db_path = Path(db_path)
        self.conn = None
    
    def connect(self):
        """Connect to DuckDB database."""
        self.conn = duckdb.connect(str(self.db_path))
        self.conn.execute("install fts;load fts;")
        # self._create_table_if_not_exists()
    
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
        
        if self.conn is None:
            self.connect()
        
        if csv_path is None:
            # Download from default URL
            print(f"Downloading data from {default_url}...")
            self.conn.execute("DELETE FROM retractions")
            self.conn.execute(f'CREATE TABLE retractions AS SELECT * FROM read_csv({default_url});')
            csv_path = str(csv_file)
        else:
            csv_file = Path(csv_path)
            if not csv_file.exists():
                raise FileNotFoundError(f"CSV file not found: {csv_path}")
            csv_source = csv_path
        
        
            print(f"Importing data from {csv_source}...")
        df.replace({pd.NA: None, np.nan: None}, inplace=True)
            
            # Clear existing data
            self.conn.execute("DELETE FROM retractions")
            
            # Import CSV directly using DuckDB's read_csv function
            import_sql = f"""
            f'CREATE TABLE retractions AS 
            SELECT * FROM read_csv({default_url});
            """
            
            self.conn.execute(import_sql)
            
        # criando índice para busca de texto completo
        self.conn.execute("""
                          PRAGMA create_fts_index('retractions', 'record_id', 'title','subject','institution','subject','author')
                          """)
        
        # Get count of imported records
        count_result = self.conn.execute("SELECT COUNT(*) FROM retractions").fetchone()
        record_count = count_result[0] if count_result else 0
        print(f"Successfully imported {record_count} records.")
        self.disconnect()
        
    
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
