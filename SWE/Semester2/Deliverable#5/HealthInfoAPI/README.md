# Health Information Network API Documentation

This document provides information about the REST APIs implemented for the Health Information Network project.

## Base URL

```
http://localhost:3000/api
```

## GET APIs

### 1. Get All Patients

Retrieves a list of all registered patients.

- **URL**: `/patients`
- **Method**: `GET`
- **Response**: Array of patient objects
- **Example Response**:
  ```json
  [
    {
      "id": "1234567890",
      "name": "John Doe",
      "age": 30,
      "gender": "male",
      "contact": "123-456-7890",
      "createdAt": "2024-03-14T12:00:00.000Z"
    }
  ]
  ```

### 2. Get Patient by ID

Retrieves a specific patient's information by their ID.

- **URL**: `/patients/:id`
- **Method**: `GET`
- **URL Parameters**: `id=[string]` (required)
- **Response**: Patient object
- **Example Response**:
  ```json
  {
    "id": "1234567890",
    "name": "John Doe",
    "age": 30,
    "gender": "male",
    "contact": "123-456-7890",
    "createdAt": "2024-03-14T12:00:00.000Z"
  }
  ```
- **Error Response**: 404 Not Found if patient doesn't exist

## POST APIs

### 1. Create New Patient

Creates a new patient record.

- **URL**: `/patients`
- **Method**: `POST`
- **Request Body**:
  ```json
  {
    "name": "John Doe",
    "age": 30,
    "gender": "male",
    "contact": "123-456-7890"
  }
  ```
- **Response**: Created patient object
- **Error Response**: 400 Bad Request if required fields are missing

### 2. Add Medical Record

Adds a new medical record for a patient.

- **URL**: `/medical-records`
- **Method**: `POST`
- **Request Body**:
  ```json
  {
    "patientId": "1234567890",
    "diagnosis": "Common cold",
    "treatment": "Rest and fluids",
    "notes": "Patient should return in 1 week if symptoms persist"
  }
  ```
- **Response**: Created medical record object
- **Error Response**: 
  - 400 Bad Request if required fields are missing
  - 404 Not Found if patient doesn't exist

## Error Responses

All APIs may return the following error responses:

- **400 Bad Request**: When required fields are missing or invalid
- **404 Not Found**: When requested resource doesn't exist
- **500 Internal Server Error**: When server encounters an error

## Testing with Postman

1. Start the server:
   ```bash
   npm install
   npm start
   ```

2. Import the following Postman collection:
   - GET http://localhost:3000/api/patients
   - GET http://localhost:3000/api/patients/:id
   - POST http://localhost:3000/api/patients
   - POST http://localhost:3000/api/medical-records

3. Test each endpoint with appropriate request bodies and parameters. 