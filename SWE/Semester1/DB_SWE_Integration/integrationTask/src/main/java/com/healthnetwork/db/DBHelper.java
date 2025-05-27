package com.healthnetwork.db;

import com.healthnetwork.model.Patient;
import java.sql.*;
import java.util.ArrayList;
import java.util.List;

public class DBHelper {
    private static final String DB_URL = "jdbc:sqlite:healthnetwork.db";

    public static void init() throws SQLException {
        try (Connection conn = DriverManager.getConnection(DB_URL);
             Statement stmt = conn.createStatement()) {
            // Create patients table if it doesn't exist
            stmt.executeUpdate("""
                CREATE TABLE IF NOT EXISTS patients (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    first_name TEXT NOT NULL,
                    last_name TEXT NOT NULL,
                    date_of_birth TEXT NOT NULL,
                    gender TEXT NOT NULL,
                    address TEXT,
                    phone_number TEXT,
                    email TEXT
                )
            """);
        }
    }

    public static List<Patient> getAllPatients() throws SQLException {
        List<Patient> patients = new ArrayList<>();
        try (Connection conn = DriverManager.getConnection(DB_URL);
             Statement stmt = conn.createStatement();
             ResultSet rs = stmt.executeQuery("SELECT * FROM patients")) {
            
            while (rs.next()) {
                Patient patient = new Patient(
                    rs.getInt("id"),
                    rs.getString("first_name"),
                    rs.getString("last_name"),
                    rs.getString("date_of_birth"),
                    rs.getString("gender"),
                    rs.getString("address"),
                    rs.getString("phone_number"),
                    rs.getString("email")
                );
                patients.add(patient);
            }
        }
        return patients;
    }

    public static Patient getPatientById(int id) throws SQLException {
        try (Connection conn = DriverManager.getConnection(DB_URL);
             PreparedStatement pstmt = conn.prepareStatement("SELECT * FROM patients WHERE id = ?")) {
            
            pstmt.setInt(1, id);
            ResultSet rs = pstmt.executeQuery();
            
            if (rs.next()) {
                return new Patient(
                    rs.getInt("id"),
                    rs.getString("first_name"),
                    rs.getString("last_name"),
                    rs.getString("date_of_birth"),
                    rs.getString("gender"),
                    rs.getString("address"),
                    rs.getString("phone_number"),
                    rs.getString("email")
                );
            }
        }
        return null;
    }

    public static void insertPatient(Patient patient) throws SQLException {
        String sql = """
            INSERT INTO patients (first_name, last_name, date_of_birth, gender, address, phone_number, email)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """;
        
        try (Connection conn = DriverManager.getConnection(DB_URL);
             PreparedStatement pstmt = conn.prepareStatement(sql)) {
            
            pstmt.setString(1, patient.getFirstName());
            pstmt.setString(2, patient.getLastName());
            pstmt.setString(3, patient.getDateOfBirth());
            pstmt.setString(4, patient.getGender());
            pstmt.setString(5, patient.getAddress());
            pstmt.setString(6, patient.getPhoneNumber());
            pstmt.setString(7, patient.getEmail());
            
            pstmt.executeUpdate();
        }
    }

    public static void updatePatient(Patient patient) throws SQLException {
        String sql = """
            UPDATE patients 
            SET first_name = ?, last_name = ?, date_of_birth = ?, gender = ?, 
                address = ?, phone_number = ?, email = ?
            WHERE id = ?
        """;
        
        try (Connection conn = DriverManager.getConnection(DB_URL);
             PreparedStatement pstmt = conn.prepareStatement(sql)) {
            
            pstmt.setString(1, patient.getFirstName());
            pstmt.setString(2, patient.getLastName());
            pstmt.setString(3, patient.getDateOfBirth());
            pstmt.setString(4, patient.getGender());
            pstmt.setString(5, patient.getAddress());
            pstmt.setString(6, patient.getPhoneNumber());
            pstmt.setString(7, patient.getEmail());
            pstmt.setInt(8, patient.getId());
            
            pstmt.executeUpdate();
        }
    }
} 