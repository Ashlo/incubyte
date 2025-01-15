from datetime import date, timedelta
import pytest
from src.models.vaccination_record import VaccinationRecord

class TestVaccinationRecord:
    @pytest.fixture
    def sample_record(self):
        return VaccinationRecord(
            customer_id="1",
            customer_name="Ashutosh Bele",
            dob=date(1996, 1, 1),
            last_consulted_date=date(2022, 1, 1),
            vaccination_id="ABC",
            dr_name="Dr. Banner",
            state="NSW",
            country="AUS"
        )
    
    def test_age_calculation(self, sample_record):
        expected_age = date.today().year - 1996
        # Adjust for birthdays not yet occurred this year
        if (date.today().month, date.today().day) < (1, 1):
            expected_age -= 1
        assert sample_record.age == expected_age
    
    def test_days_since_last_consulted(self, sample_record):
        expected_days = (date.today() - date(2022, 1, 1)).days
        assert sample_record.days_since_last_consulted == expected_days
    
    def test_null_dates_handling(self):
        record = VaccinationRecord(
            customer_id="2",
            customer_name="Elon Musk",
            dob=None,
            last_consulted_date=None,
            vaccination_id="XYZ",
            dr_name=None,
            state=None,
            country="AUS"
        )
        assert record.age is None
        assert record.days_since_last_consulted is None 
    
    def test_needs_consultation(self, sample_record):
        # Set last consultation to more than 30 days ago
        old_date = date.today() - timedelta(days=31)
        sample_record.last_consulted_date = old_date
        assert sample_record.needs_consultation is True
        
        # Set last consultation to less than 30 days ago
        recent_date = date.today() - timedelta(days=15)
        sample_record.last_consulted_date = recent_date
        assert sample_record.needs_consultation is False 