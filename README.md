# Patient Management API

A RESTful API built with FastAPI for managing patient records with automatic BMI calculation and health status assessment.

## Features

- **CRUD Operations**: Create, Read, Update, and Delete patient records
- **Automatic BMI Calculation**: Computes BMI based on height and weight
- **Health Status Verdict**: Automatically categorizes patients as UnderWeight, Normal, OverWeight, or Obese
- **Data Validation**: Uses Pydantic for robust input validation
- **JSON Storage**: Persistent data storage using JSON file
- **Interactive API Documentation**: Auto-generated docs via FastAPI

## Technologies Used

- **FastAPI**: Modern, fast web framework for building APIs
- **Pydantic**: Data validation using Python type annotations
- **Uvicorn**: ASGI server for running the application
- **Python 3.13**: Latest Python version

## Installation

1. Clone the repository:
```bash
git clone <your-repo-url>
cd FastAPI
```

2. Create and activate virtual environment:
```bash
python -m venv myenv
myenv\Scripts\activate  # Windows
```

3. Install dependencies:
```bash
pip install fastapi uvicorn pydantic
```

## Usage

1. Start the server:
```bash
uvicorn main:app --reload
```

2. Access the API:
   - API Base URL: `http://127.0.0.1:8000`
   - Interactive Docs: `http://127.0.0.1:8000/docs`
   - Alternative Docs: `http://127.0.0.1:8000/redoc`

## API Endpoints

### General Endpoints

- **GET** `/` - Welcome message
- **GET** `/about` - API description
- **GET** `/time` - Current server time

### Patient Management

- **GET** `/view` - View all patients
- **GET** `/patient/{patient_id}` - View specific patient by ID
- **POST** `/create` - Create a new patient record
- **PUT** `/edit/{patient_id}` - Update existing patient record
- **DELETE** `/delete/{patient_id}` - Delete patient record

## Patient Data Model

```json
{
  "id": "P001",
  "name": "John Doe",
  "city": "New York",
  "age": 30,
  "gender": "male",
  "height": 1.75,
  "weight": 70.0
}
```

### Computed Fields

- **bmi**: Automatically calculated as `weight / (height²)`
- **verdict**: Health status based on BMI:
  - BMI < 18.5: UnderWeight
  - BMI 18.5-25: Normal
  - BMI 25-30: OverWeight
  - BMI > 30: Obese

## Example Requests

### Create a Patient
```bash
POST http://127.0.0.1:8000/create
Content-Type: application/json

{
  "id": "P001",
  "name": "John Doe",
  "city": "New York",
  "age": 30,
  "gender": "male",
  "height": 1.75,
  "weight": 70.0
}
```

### Update a Patient
```bash
PUT http://127.0.0.1:8000/edit/P001
Content-Type: application/json

{
  "weight": 75.0
}
```

### Delete a Patient
```bash
DELETE http://127.0.0.1:8000/delete/P001
```

## Project Structure

```
FastAPI/
├── main.py           # Main application file
├── patients.json     # Patient data storage
├── myenv/           # Virtual environment
└── README.md        # This file
```

## Data Validation

The API uses Pydantic for data validation:
- **ID**: Required string (e.g., "P001")
- **Name**: Required string
- **City**: Required string
- **Age**: Required integer (must be positive)
- **Gender**: Must be one of: "male", "female", "others"
- **Height**: Required float in meters (must be > 0)
- **Weight**: Required float in kilograms (must be > 0)

## Error Handling

- **400 Bad Request**: Patient already exists
- **404 Not Found**: Patient ID doesn't exist
- **422 Unprocessable Entity**: Invalid data format

## Contributing

Feel free to fork this project and submit pull requests for any improvements.

## License

This project is open source and available under the MIT License.

## Author

Created as a learning project to demonstrate FastAPI capabilities.
