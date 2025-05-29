package org.example.api;

// Bridge Pattern Implementation for Medical Records Management

// Implementer Interface
interface MedicalRecordStorage {
    void saveRecord(String data);
    String retrieveRecord(String id);
}

// Concrete Implementer 1
class DatabaseStorage implements MedicalRecordStorage {
    @Override
    public void saveRecord(String data) {
        System.out.println("Saving record to database: " + data);
    }

    @Override
    public String retrieveRecord(String id) {
        return "Retrieved record from database with ID: " + id;
    }
}

// Concrete Implementer 2
class FileStorage implements MedicalRecordStorage {
    @Override
    public void saveRecord(String data) {
        System.out.println("Saving record to file system: " + data);
    }

    @Override
    public String retrieveRecord(String id) {
        return "Retrieved record from file system with ID: " + id;
    }
}

// Abstraction
abstract class MedicalRecord {
    protected MedicalRecordStorage storage;

    public MedicalRecord(MedicalRecordStorage storage) {
        this.storage = storage;
    }

    abstract void save();
    abstract String retrieve(String id);
}

// Refined Abstraction 1
class PatientRecord extends MedicalRecord {
    private String patientData;

    public PatientRecord(MedicalRecordStorage storage, String patientData) {
        super(storage);
        this.patientData = patientData;
    }

    @Override
    void save() {
        storage.saveRecord("Patient Record: " + patientData);
    }

    @Override
    String retrieve(String id) {
        return storage.retrieveRecord(id);
    }
}

// Refined Abstraction 2
class DoctorRecord extends MedicalRecord {
    private String doctorData;

    public DoctorRecord(MedicalRecordStorage storage, String doctorData) {
        super(storage);
        this.doctorData = doctorData;
    }

    @Override
    void save() {
        storage.saveRecord("Doctor Record: " + doctorData);
    }

    @Override
    String retrieve(String id) {
        return storage.retrieveRecord(id);
    }
}

// Main class to demonstrate the Bridge Pattern
public class Client {
    public static void main(String[] args) {
        // Create storage implementations
        MedicalRecordStorage dbStorage = new DatabaseStorage();
        MedicalRecordStorage fileStorage = new FileStorage();

        // Create medical records with different storage implementations
        MedicalRecord patientRecordDB = new PatientRecord(dbStorage, "John Doe, Age: 30");
        MedicalRecord patientRecordFile = new PatientRecord(fileStorage, "Jane Smith, Age: 25");
        MedicalRecord doctorRecordDB = new DoctorRecord(dbStorage, "Dr. Smith, Specialty: Cardiology");
        MedicalRecord doctorRecordFile = new DoctorRecord(fileStorage, "Dr. Johnson, Specialty: Neurology");

        // Demonstrate the bridge pattern
        System.out.println("Saving records:");
        patientRecordDB.save();
        patientRecordFile.save();
        doctorRecordDB.save();
        doctorRecordFile.save();

        System.out.println("\nRetrieving records:");
        System.out.println(patientRecordDB.retrieve("P001"));
        System.out.println(patientRecordFile.retrieve("P002"));
        System.out.println(doctorRecordDB.retrieve("D001"));
        System.out.println(doctorRecordFile.retrieve("D002"));
    }
}

