import logging
from pathlib import Path
import sqlite3
from tabulate import tabulate
from src.database.db_handler import DatabaseHandler
from src.services.vaccination_processor import VaccinationProcessor
from src.demo.sample_data_generator import create_sample_data

def view_tables(db_path: str = "demo_hospital.db"):
    """View contents of all tables in the database"""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Get all tables
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    
    for table in tables:
        table_name = table[0]
        print(f"\n=== Table: {table_name} ===")
        
        # Get column names
        cursor.execute(f"PRAGMA table_info({table_name});")
        columns = [col[1] for col in cursor.fetchall()]
        
        # Get data
        cursor.execute(f"SELECT * FROM {table_name}")
        rows = cursor.fetchall()
        
        if rows:
            print(tabulate(rows, headers=columns, tablefmt='grid'))
        else:
            print("(Empty table)")
    
    conn.close()

def run_demo():
    # Set up logging
    logging.basicConfig(level=logging.INFO,
                       format='%(asctime)s - %(levelname)s - %(message)s')
    
    # Create sample data file
    data_dir = Path("demo_data")
    data_dir.mkdir(exist_ok=True)
    sample_file = data_dir / "sample_vaccination_data.txt"
    create_sample_data(sample_file)
    
    # Initialize database and processor
    logging.info("Initializing database...")
    db_handler = DatabaseHandler("sqlite:///demo_hospital.db")
    processor = VaccinationProcessor(db_handler)
    
    print("\n=== Hospital Vaccination Data Processing Demo ===\n")
    logging.info("Starting data processing...")
    
    try:
        # Process the file
        result = processor.process_file(str(sample_file))
        
        # Print processing summary
        print("\n=== Processing Summary ===")
        print(f"Records processed: {result['processed']}")
        print(f"Valid records: {result['valid']}")
        print(f"Errors found: {result['errors']}")
        
        # View database contents
        print("\n=== Database Contents ===")
        view_tables()
        
        if result['errors'] > 0:
            print("\n=== Validation Errors ===")
            for error in result['error_details']:
                print(f"Record {error.record_id}: {error.field} - {error.message}")
        
        # Display country-specific results
        print("\n=== Records by Country ===")
        for country in ['USA', 'IND', 'AUS']:
            records = db_handler.get_country_records(country)
            if records:  # Only show countries with records
                print(f"\n{country}:")
                for record in records:
                    print(f"• {record['customer_name']} (ID: {record['customer_id']})")
                    print(f"  - Last consulted: {record['last_consulted_date']}")
                    print(f"  - Days since consultation: {record['days_since_consulted']}")
                    print(f"  - Needs consultation: {'Yes' if record['needs_consultation'] else 'No'}")
        
        print("\n=== Demo Completed Successfully ===\n")
        
    except Exception as e:
        logging.error(f"Demo failed: {str(e)}")
        raise

if __name__ == "__main__":
    run_demo() 