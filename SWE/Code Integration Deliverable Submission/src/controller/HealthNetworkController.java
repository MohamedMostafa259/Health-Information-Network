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
        String query = "SELECT * FROM Patient";
        try (PreparedStatement stmt = connection.prepareStatement(query);
             ResultSet rs = stmt.executeQuery()) {
            while (rs.next()) {
                Patient patient = new Patient();
                patient.setPatientID(rs.getInt("PatientID"));
                patient.setName(rs.getString("Name"));
                patient.setPhoneNo(rs.getString("PhoneNo"));
                patient.setNationalID(rs.getString("NationalID"));
                patient.setInsuranceStatus(rs.getBoolean("InsuranceStatus"));
                patient.setBirthdate(rs.getString("Birthdate"));
                patient.setGender(rs.getString("Gender"));
                patient.setEmail(rs.getString("Email"));
                patient.setAge(rs.getInt("Age"));
                patient.setInsuranceID(rs.getInt("InsuranceID"));
                patient.setPackageID(rs.getInt("PackageID"));
                patients.add(patient);
            }
        } catch (SQLException e) {
            e.printStackTrace();
        }
        return patients;
    }
}