import logging
from typing import List
from src.services.file_parser import FileParser
from src.services.validator import VaccinationRecordValidator
from src.database.db_handler import DatabaseHandler

class VaccinationProcessor:
    def __init__(self, db_handler: DatabaseHandler):
        self.parser = FileParser()
        self.validator = VaccinationRecordValidator()
        self.db_handler = db_handler
        
    def process_file(self, filepath: str) -> dict:
        """Process a single vaccination data file"""
        logging.info(f"Processing file: {filepath}")
        
        try:
            # Parse records from file
            records = self.parser.parse_file(filepath)
            
            # Validate records
            valid_records = []
            errors = []
            for record in records:
                validation_errors = self.validator.validate(record)
                if validation_errors:
                    errors.extend(validation_errors)
                else:
                    valid_records.append(record)
            
            # Load valid records to database
            if valid_records:
                self.db_handler.load_to_staging(valid_records)
                self.db_handler.distribute_to_country_tables()
            
            return {
                'processed': len(records),
                'valid': len(valid_records),
                'errors': len(errors),
                'error_details': errors
            }
            
        except Exception as e:
            logging.error(f"Error processing file {filepath}: {str(e)}")
            raise 