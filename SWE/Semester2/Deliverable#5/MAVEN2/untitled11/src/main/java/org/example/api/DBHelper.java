package org.example.api;

import java.sql.*;
import java.util.ArrayList;
import java.util.List;

public class DBHelper {
    private static final String DB_URL = "jdbc:sqlite:students.db";

    public static void init() throws SQLException {
        try (Connection conn = DriverManager.getConnection(DB_URL);
             Statement stmt = conn.createStatement()) {
            stmt.executeUpdate("CREATE TABLE IF NOT EXISTS doctors (id INTEGER PRIMARY KEY, name TEXT, specialty TEXT)");
            stmt.executeUpdate("CREATE TABLE IF NOT EXISTS patients (id INTEGER PRIMARY KEY, name TEXT, illness TEXT)");
        }
    }

    public static void insertDoctor(Doctor d) throws SQLException {
        String sql = "INSERT INTO doctors(name, specialty) VALUES(?, ?)";
        try (Connection conn = DriverManager.getConnection(DB_URL);
             PreparedStatement pstmt = conn.prepareStatement(sql)) {
            pstmt.setString(1, d.name);
            pstmt.setString(2, d.specialty);
            pstmt.executeUpdate();
        }
    }

    public static List<Doctor> getAllDoctors() throws SQLException {
        List<Doctor> list = new ArrayList<>();
        try (Connection conn = DriverManager.getConnection(DB_URL);
             Statement stmt = conn.createStatement();
             ResultSet rs = stmt.executeQuery("SELECT * FROM doctors")) {
            while (rs.next()) {
                list.add(new Doctor(rs.getInt("id"), rs.getString("name"), rs.getString("specialty")));
            }
        }
        return list;
    }

    public static void insertPatient(Patient p) throws SQLException {
        String sql = "INSERT INTO patients(name, illness) VALUES(?, ?)";
        try (Connection conn = DriverManager.getConnection(DB_URL);
             PreparedStatement pstmt = conn.prepareStatement(sql)) {
            pstmt.setString(1, p.name);
            pstmt.setString(2, p.illness);
            pstmt.executeUpdate();
        }
    }

    public static List<Patient> getAllPatients() throws SQLException {
        List<Patient> list = new ArrayList<>();
        try (Connection conn = DriverManager.getConnection(DB_URL);
             Statement stmt = conn.createStatement();
             ResultSet rs = stmt.executeQuery("SELECT * FROM patients")) {
            while (rs.next()) {
                list.add(new Patient(rs.getInt("id"), rs.getString("name"), rs.getString("illness")));
            }
        }
        return list;
    }
}
