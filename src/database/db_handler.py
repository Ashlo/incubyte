from typing import List
import os
import pandas as pd
import numpy as np
from sqlalchemy import create_engine, text
from src.models.vaccination_record import VaccinationRecord
from pkg_resources import resource_string

class DatabaseHandler:
    def __init__(self, connection_string: str):
        self.engine = create_engine(connection_string, future=True)
        self._create_tables()
        
    def _create_tables(self):
        """Create tables using SQL file"""
        try:
            # Read SQL file from package resources
            sql = resource_string('src.database', 'create_tables.sql').decode('utf-8')
            
            # Execute each statement
            with self.engine.begin() as conn:
                for statement in sql.split(';'):
                    if statement.strip():
                        conn.execute(text(statement))
        except Exception as e:
            print(f"Error creating tables: {str(e)}")
            raise
    
    def load_to_staging(self, records: List[VaccinationRecord]):
        """Load records to staging table with computed columns"""
        data = []
        for record in records:
            data.append({
                'customer_id': record.customer_id,
                'customer_name': record.customer_name,
                'open_date': record.open_date,
                'last_consulted_date': record.last_consulted_date,
                'vaccination_id': record.vaccination_id,
                'dr_name': record.dr_name,
                'state': record.state,
                'country': record.country,
                'dob': record.dob,
                'is_active': record.is_active,
                'age': record.age,  # Use computed property
                'days_since_last_consulted': record.days_since_last_consulted,  # Use computed property
                'needs_consultation': 1 if record.needs_consultation else 0  # Use computed property
            })
        
        df = pd.DataFrame(data)
        df.to_sql('staging_vaccination_records', self.engine, 
                  if_exists='append', index=False)
    
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