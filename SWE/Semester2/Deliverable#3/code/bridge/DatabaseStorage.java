package com.healthinformationnetwork.patterns.bridge;

public class DatabaseStorage implements MedicalRecordStorage {
    @Override
    public void saveRecord(String patientId, String recordData) {
        // Implementation for saving to database
        System.out.println("Saving record for patient " + patientId + " to database");
    }

    @Override
    public String retrieveRecord(String patientId) {
        // Implementation for retrieving from database
        System.out.println("Retrieving record for patient " + patientId + " from database");
        return "Record data from database";
    }

    @Override
    public void deleteRecord(String patientId) {
        // Implementation for deleting from database
        System.out.println("Deleting record for patient " + patientId + " from database");
    }
} 