    """
    Extracts and updates a duckdb database based on the data From Retraction Watch:
    https://gitlab.com/crossref/retraction-watch-data/-/blob/main/retraction_watch.csv
    """
    import duckdb
    from pydantic import BaseModel
    
    
    # Using a data model built with pydantic Basemodel to reflect the data in the retraction watch CSV, create a class that imports the data to a duckdb file, if it does not exist or updates it, if an updated CSV is available. AI!
    
    