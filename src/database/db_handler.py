from typing import List
import os
import pandas as pd
import numpy as np
from sqlalchemy import create_engine, text
from src.models.vaccination_record import VaccinationRecord

class DatabaseHandler:
    def __init__(self, connection_string: str):
        self.engine = create_engine(connection_string, future=True)
        self._create_tables()
        
    def _create_tables(self):
        """Create tables using SQL file"""
        # Get the path to the SQL file
        current_dir = os.path.dirname(os.path.abspath(__file__))
        sql_file_path = os.path.join(current_dir, 'create_tables.sql')
        
        # Read and execute the SQL file
        with open(sql_file_path, 'r') as file:
            sql_statements = file.read()
            
        # Split and execute each statement
        with self.engine.begin() as conn:
            # SQLite doesn't support multiple statements in one execute
            for statement in sql_statements.split(';'):
                if statement.strip():
                    # Replace MySQL/PostgreSQL specific syntax with SQLite syntax
                    statement = statement.replace('DATEDIFF(day,', 'julianday(') \
                                       .replace('YEAR(CURRENT_DATE)', "strftime('%Y', 'now')") \
                                       .replace('YEAR(', "strftime('%Y', ")
                    conn.execute(text(statement))
    
    def load_to_staging(self, records: List[VaccinationRecord], batch_size: int = 1000):
        """Load records to staging table in batches"""
        # Clear staging table first
        with self.engine.begin() as conn:
            conn.execute(text("DELETE FROM staging_vaccination_records"))
            
        df = pd.DataFrame([vars(record) for record in records])
        
        # Load data in chunks to handle large volumes
        for chunk in np.array_split(df, max(1, len(df) // batch_size)):
            chunk.to_sql('staging_vaccination_records', 
                        self.engine, 
                        if_exists='append', 
                        index=False)
    
    def distribute_to_country_tables(self):
        """Distribute records to country-specific tables"""
        with self.engine.begin() as conn:
            # Clear country tables first
            for country in ['IND', 'USA', 'AUS']:
                conn.execute(text(f"DELETE FROM table_{country.lower()}"))
                
            # Insert records from staging
            for country in ['IND', 'USA', 'AUS']:
                upsert_query = text(f"""
                    INSERT INTO table_{country.lower()}
                    SELECT * FROM staging_vaccination_records 
                    WHERE country = :country
                    AND (customer_id, last_consulted_date) IN (
                        SELECT customer_id, MAX(last_consulted_date)
                        FROM staging_vaccination_records
                        WHERE country = :country
                        GROUP BY customer_id
                    )
                """)
                conn.execute(upsert_query, {'country': country})
                
    def get_country_records(self, country: str):
        """Get records for a specific country with computed columns"""
        query = text(f"""
            SELECT 
                customer_id, 
                customer_name, 
                last_consulted_date,
                CAST(julianday('now') - julianday(last_consulted_date) AS INTEGER) as days_since_consulted,
                CASE 
                    WHEN julianday('now') - julianday(last_consulted_date) > 30 
                    THEN 1 
                    ELSE 0 
                END as needs_consultation
            FROM table_{country.lower()}
        """)
        with self.engine.connect() as conn:
            return [dict(row) for row in conn.execute(query)] 