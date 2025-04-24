package com.healthinformationnetwork.patterns.bridge;

public interface MedicalRecordStorage {
    void saveRecord(String patientId, String recordData);
    String retrieveRecord(String patientId);
    void deleteRecord(String patientId);
} 