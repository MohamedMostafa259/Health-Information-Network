# Health Information Network API

This is a Spring Boot application that provides REST APIs for managing patient information and medical records.

## Prerequisites

- Java 17 or higher
- Maven 3.6 or higher

## Getting Started

1. Clone the repository
2. Navigate to the project directory
3. Run the application:
   ```bash
   mvn spring-boot:run
   ```
4. The application will start on port 8080

## API Documentation

Base URL: `http://localhost:8080/api`

### GET APIs

#### 1. Get All Patients
- **Endpoint**: `GET /patients`
- **Description**: Retrieves a list of all registered patients
- **Response**: Array of patient objects
- **Example Response**:
  ```json
  [
    {
      "id": 1,
      "name": "John Doe",
      "age": 30,
      "gender": "MALE",
      "contactInfo": "john@example.com"
    }
  ]
  ```

#### 2. Get Patient by ID
- **Endpoint**: `GET /patients/{id}`
- **Description**: Retrieves a specific patient's information
- **Parameters**: 
  - `id` (path parameter): Patient ID
- **Response**: Patient object
- **Example Response**:
  ```json
  {
    "id": 1,
    "name": "John Doe",
    "age": 30,
    "gender": "MALE",
    "contactInfo": "john@example.com"
  }
  ```

### POST APIs

#### 1. Create New Patient
- **Endpoint**: `POST /patients`
- **Description**: Creates a new patient record
- **Request Body**:
  ```json
  {
    "name": "John Doe",
    "age": 30,
    "gender": "MALE",
    "contactInfo": "john@example.com"
  }
  ```
- **Response**: Created patient object

#### 2. Add Medical Record
- **Endpoint**: `POST /medical-records`
- **Description**: Adds a new medical record for a patient
- **Request Body**:
  ```json
  {
    "patient": {
      "id": 1
    },
    "diagnosis": "Common cold",
    "treatment": "Rest and medication",
    "notes": "Patient should rest for 3 days"
  }
  ```
- **Response**: Created medical record object

## Error Responses

- **400 Bad Request**: Invalid input data
- **404 Not Found**: Resource not found
- **500 Internal Server Error**: Server-side error

## Database

The application uses an H2 in-memory database. You can access the H2 console at:
`http://localhost:8080/h2-console`

- JDBC URL: `jdbc:h2:mem:healthdb`
- Username: `sa`
- Password: (empty) 