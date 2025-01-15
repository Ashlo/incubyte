from dataclasses import dataclass
from typing import List
from src.models.vaccination_record import VaccinationRecord

@dataclass
class ValidationError:
    field: str
    message: str
    record_id: str

class VaccinationRecordValidator:
    def validate(self, record: VaccinationRecord) -> List[ValidationError]:
        errors = []
        
        # Required field validations
        if not record.customer_name or len(record.customer_name) > 255:
            errors.append(ValidationError(
                'customer_name',
                'Customer name is required and must not exceed 255 characters',
                record.customer_id
            ))
            
        if not record.customer_id or len(record.customer_id) > 18:
            errors.append(ValidationError(
                'customer_id',
                'Customer ID is required and must not exceed 18 characters',
                record.customer_id
            ))
            
        if not record.open_date:
            errors.append(ValidationError(
                'open_date',
                'Open date is required',
                record.customer_id
            ))
            
        # Optional field length validations
        if record.vaccination_id and len(record.vaccination_id) > 5:
            errors.append(ValidationError(
                'vaccination_id',
                'Vaccination ID must not exceed 5 characters',
                record.customer_id
            ))
            
        return errors 