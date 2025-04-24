package com.healthinformationnetwork.patterns.bridge;

public class FileSystemStorage implements MedicalRecordStorage {
    @Override
    public void saveRecord(String patientId, String recordData) {
        // Implementation for saving to file system
        System.out.println("Saving record for patient " + patientId + " to file system");
    }

    @Override
    public String retrieveRecord(String patientId) {
        // Implementation for retrieving from file system
        System.out.println("Retrieving record for patient " + patientId + " from file system");
        return "Record data from file system";
    }

    @Override
    public void deleteRecord(String patientId) {
        // Implementation for deleting from file system
        System.out.println("Deleting record for patient " + patientId + " from file system");
    }
} 