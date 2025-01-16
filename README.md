# Hospital Vaccination Data Processor

A Python-based ETL system for processing and managing vaccination records across a global hospital chain. (Incubyte assessment)

## Features

- Parse vaccination records from standardized text files
- Validate and process customer data with proper error handling
- Distribute records to country-specific database tables
- Calculate derived metrics like age and consultation status
- Handle large-scale data processing with batch operations
- Track customer movement between countries

## Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

## Installation

1. Clone the repository:
bash
git clone <repository-url>
cd incubyte

2. Create and activate a virtual environment (recommended):
bash
python -m venv venv
source venv/bin/activate # On Windows: venv\Scripts\activate

3. Install the package and dependencies:
```bash
pip install -e .
```

### Project Structure

The project structure is organized as follows:

* `src/`: This directory contains the source code for the project.
	+ `database/`: Handles database operations and SQL scripts.
	+ `models/`: Defines data models and entities.
	+ `services/`: Implements core business logic.
	+ `demo/`: A demo application showcasing the project's functionality.
* `tests/`: Contains unit tests for the project.
* `requirements.txt`: Lists project dependencies.
* `setup.py`: Configures the project package.

## Usage

### Running the Demo

The project includes a demo application that showcases the main functionality:

```python
from src.demo.demo import run_demo
run_demo()
```

### Processing Vaccination Records
```python
from src.database.db_handler import DatabaseHandler
from src.services.vaccination_processor import VaccinationProcessor

# Initialize components
db_handler = DatabaseHandler("sqlite:///hospital.db")
processor = VaccinationProcessor(db_handler)

# Process a data file
result = processor.process_file("path/to/vaccination_data.txt")
```

## Data Format

The system expects input files in the following format:

```
|H|Customer_Name|Customer_Id|Open_Date|Last_Consulted_Date|Vaccination_Id|Dr_Name|State|Country|DOB|Is_Active
|D|John|123456|20101012|20121013|MVD|Paul|NSW|AU|06031987|A
```

### Field Specifications
```
- Customer_Name: VARCHAR(255), Required
- Customer_Id: VARCHAR(18), Required
- Open_Date: DATE (YYYYMMDD), Required
- Last_Consulted_Date: DATE (YYYYMMDD)
- Vaccination_Id: CHAR(5)
- Dr_Name: VARCHAR(255)
- State: CHAR(5)
- Country: CHAR(5)
- DOB: DATE (YYYYMMDD)
- Is_Active: CHAR(1)
```

## Testing

Run the test suite:
```bash
pytest
```

## License

This project is open-sourced under the MIT License - see the LICENSE file for details.


