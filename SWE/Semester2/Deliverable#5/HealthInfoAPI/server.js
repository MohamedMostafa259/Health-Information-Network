const express = require('express');
const cors = require('cors');
const bodyParser = require('body-parser');

const app = express();
const port = 3000;

// Middleware
app.use(cors());
app.use(bodyParser.json());

// In-memory data store (replace with database in production)
let patients = [];
let medicalRecords = [];

// GET APIs

// 1. Get all patients
app.get('/api/patients', (req, res) => {
    res.json(patients);
});

// 2. Get patient by ID
app.get('/api/patients/:id', (req, res) => {
    const patient = patients.find(p => p.id === req.params.id);
    if (!patient) {
        return res.status(404).json({ message: 'Patient not found' });
    }
    res.json(patient);
});

// POST APIs

// 1. Create new patient
app.post('/api/patients', (req, res) => {
    const { name, age, gender, contact } = req.body;
    
    if (!name || !age || !gender || !contact) {
        return res.status(400).json({ message: 'All fields are required' });
    }

    const newPatient = {
        id: Date.now().toString(),
        name,
        age,
        gender,
        contact,
        createdAt: new Date()
    };

    patients.push(newPatient);
    res.status(201).json(newPatient);
});

// 2. Add medical record
app.post('/api/medical-records', (req, res) => {
    const { patientId, diagnosis, treatment, notes } = req.body;

    if (!patientId || !diagnosis || !treatment) {
        return res.status(400).json({ message: 'Patient ID, diagnosis, and treatment are required' });
    }

    const patient = patients.find(p => p.id === patientId);
    if (!patient) {
        return res.status(404).json({ message: 'Patient not found' });
    }

    const newRecord = {
        id: Date.now().toString(),
        patientId,
        diagnosis,
        treatment,
        notes,
        createdAt: new Date()
    };

    medicalRecords.push(newRecord);
    res.status(201).json(newRecord);
});

// Start server
app.listen(port, () => {
    console.log(`Server running at http://localhost:${port}`);
}); 