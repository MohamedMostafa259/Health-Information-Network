package controller;

import model.DatabaseConnection;
import model.Patient;

import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.util.ArrayList;
import java.util.List;

public class HealthNetworkController {
    private Connection connection;

    public HealthNetworkController() {
        connection = DatabaseConnection.getConnection();
    }

    public List<Patient> getAllPatients() {
        List<Patient> patients = new ArrayList<>();
        String query = "SELECT * FROM Patient WHERE PatientID IS NOT NULL";
        
        try (PreparedStatement stmt = connection.prepareStatement(query);
             ResultSet rs = stmt.executeQuery()) {
            
            while (rs.next()) {
                Patient patient = new Patient();
                patient.setPatientID(rs.getString("PatientID"));
                patient.setName(rs.getString("Name"));
                patient.setPhoneNo(rs.getString("PhoneNo"));
                patient.setNationalID(rs.getString("NationalID"));
                patient.setInsuranceStatus(rs.getBoolean("InsuranceStatus"));
                patient.setBirthdate(rs.getString("Birthdate"));
                patient.setGender(rs.getString("Gender"));
                patient.setEmail(rs.getString("Email"));
                patient.setAge(rs.getInt("Age"));
                patient.setInsuranceID(rs.getString("InsuranceID"));
                patient.setPackageID(rs.getString("PackageID"));
                patients.add(patient);
            }
        } catch (SQLException e) {
            System.err.println("Error getting patients: " + e.getMessage());
            e.printStackTrace();
        }
        return patients;
    }

    public boolean addPatient(Patient patient) {
        if (connection == null) {
            System.err.println("No database connection!");
            return false;
        }

        String query = """
            INSERT INTO Patient (PatientID, Name, PhoneNo, NationalID, InsuranceStatus, 
                               Birthdate, Gender, Email, Age, InsuranceID, PackageID)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """;
        
        try (PreparedStatement stmt = connection.prepareStatement(query)) {
            stmt.setString(1, patient.getPatientID());
            stmt.setString(2, patient.getName());
            stmt.setString(3, patient.getPhoneNo());
            stmt.setString(4, patient.getNationalID());
            stmt.setInt(5, patient.isInsuranceStatus() ? 1 : 0);
            stmt.setString(6, patient.getBirthdate());
            stmt.setString(7, patient.getGender());
            stmt.setString(8, patient.getEmail());
            stmt.setInt(9, patient.getAge());
            stmt.setString(10, patient.getInsuranceID());
            stmt.setString(11, patient.getPackageID());
            
            int result = stmt.executeUpdate();
            System.out.println("Rows affected: " + result);  // debug output
            return result > 0;
        } catch (SQLException e) {
            System.err.println("Error adding patient: " + e.getMessage());
            System.err.println("SQL State: " + e.getSQLState());
            System.err.println("Error Code: " + e.getErrorCode());
            e.printStackTrace();
            return false;
        } 
    }
}