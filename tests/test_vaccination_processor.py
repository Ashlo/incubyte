import pytest
from datetime import date
from src.services.vaccination_processor import VaccinationProcessor
from src.database.db_handler import DatabaseHandler

class TestVaccinationProcessor:
    @pytest.fixture
    def processor(self):
        db_handler = DatabaseHandler("sqlite:///:memory:")  # Use in-memory DB for testing
        return VaccinationProcessor(db_handler)
    
    def test_process_file(self, processor, tmp_path):
        # Create a test file
        test_file = tmp_path / "test_data.txt"
        test_file.write_text(
            "|H|Customer_Name|Customer_Id|Open_Date|Last_Consulted_Date|Vaccination_Id|Dr_Name|State|Country|DOB|Is_Active\n"
            "|D|John|123456|20101012|20121013|MVD|Paul|NSW|AUS|06031987|A\n"
        )
        
        result = processor.process_file(str(test_file))
        
        assert result['processed'] == 1
        assert result['valid'] == 1
        assert result['errors'] == 0 