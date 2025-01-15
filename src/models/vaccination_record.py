from dataclasses import dataclass
from datetime import date
from typing import Optional

@dataclass
class VaccinationRecord:
    customer_id: str
    customer_name: str
    open_date: date
    dob: Optional[date]
    last_consulted_date: Optional[date]
    vaccination_id: Optional[str]
    dr_name: Optional[str]
    state: Optional[str]
    country: str
    is_active: Optional[str]
    
    @property
    def age(self) -> Optional[int]:
        if not self.dob:
            return None
        today = date.today()
        return today.year - self.dob.year - ((today.month, today.day) < (self.dob.month, self.dob.day))
    
    @property
    def days_since_last_consulted(self) -> Optional[int]:
        if not self.last_consulted_date:
            return None
        return (date.today() - self.last_consulted_date).days
        
    @property
    def needs_consultation(self) -> bool:
        """Check if customer needs consultation (>30 days since last visit)"""
        days = self.days_since_last_consulted
        return days is not None and days > 30
    
