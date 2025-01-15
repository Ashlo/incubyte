from datetime import datetime, date
from typing import List, Optional
from src.models.vaccination_record import VaccinationRecord

class FileParser:
    def parse_date(self, date_str: str) -> Optional[date]:
        """Parse date in YYYYMMDD format"""
        try:
            return datetime.strptime(date_str, '%Y%m%d').date()
        except (ValueError, TypeError):
            return None
            
    def parse_file(self, filepath: str) -> List[VaccinationRecord]:
        records = []
        with open(filepath, 'r') as file:
            header = file.readline()  # Skip header line
            
            for line in file:
                if line.startswith('|D|'):
                    fields = line.strip().split('|')
                    if len(fields) >= 11:  # Ensure we have all fields
                        record = VaccinationRecord(
                            customer_name=fields[2],
                            customer_id=fields[3],
                            open_date=self.parse_date(fields[4]),
                            last_consulted_date=self.parse_date(fields[5]),
                            vaccination_id=fields[6],
                            dr_name=fields[7],
                            state=fields[8],
                            country=fields[9],
                            dob=self.parse_date(fields[10]),
                            is_active=fields[11] if len(fields) > 11 else 'A'
                        )
                        records.append(record)
        return records 