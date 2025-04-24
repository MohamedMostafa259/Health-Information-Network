package com.healthinformationnetwork.patterns.adapter;

public class ExternalAPIAdapter implements HealthcareService {
    private ExternalHealthcareAPI externalAPI;

    public ExternalAPIAdapter(ExternalHealthcareAPI externalAPI) {
        this.externalAPI = externalAPI;
    }

    @Override
    public PatientData getPatientData(String patientId) {
        // Convert external API response to our system's format
        ExternalPatientData externalData = externalAPI.fetchPatientInfo(patientId);
        return convertToInternalFormat(externalData);
    }

    private PatientData convertToInternalFormat(ExternalPatientData externalData) {
        // Implementation of conversion logic
        PatientData internalData = new PatientData();
        internalData.setPatientId(externalData.getId());
        internalData.setName(externalData.getFullName());
        internalData.setMedicalHistory(externalData.getHistory());
        return internalData;
    }
}

// External API interface
interface ExternalHealthcareAPI {
    ExternalPatientData fetchPatientInfo(String patientId);
}

// Our system's interface
interface HealthcareService {
    PatientData getPatientData(String patientId);
}

// Data transfer objects
class ExternalPatientData {
    private String id;
    private String fullName;
    private String history;

    public String getId() { return id; }
    public void setId(String id) { this.id = id; }
    public String getFullName() { return fullName; }
    public void setFullName(String fullName) { this.fullName = fullName; }
    public String getHistory() { return history; }
    public void setHistory(String history) { this.history = history; }
}

class PatientData {
    private String patientId;
    private String name;
    private String medicalHistory;

    public String getPatientId() { return patientId; }
    public void setPatientId(String patientId) { this.patientId = patientId; }
    public String getName() { return name; }
    public void setName(String name) { this.name = name; }
    public String getMedicalHistory() { return medicalHistory; }
    public void setMedicalHistory(String medicalHistory) { this.medicalHistory = medicalHistory; }
} 