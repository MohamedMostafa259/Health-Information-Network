package com.healthnetwork.handler;

import com.google.gson.Gson;
import com.healthnetwork.db.DBHelper;
import com.healthnetwork.model.Patient;
import com.sun.net.httpserver.HttpExchange;
import com.sun.net.httpserver.HttpHandler;

import java.io.IOException;
import java.io.InputStreamReader;
import java.io.OutputStream;
import java.nio.charset.StandardCharsets;
import java.sql.SQLException;
import java.util.List;

public class PatientHandler implements HttpHandler {
    private final Gson gson = new Gson();

    @Override
    public void handle(HttpExchange exchange) throws IOException {
        try {
            String path = exchange.getRequestURI().getPath();
            String method = exchange.getRequestMethod();

            // Handle GET requests
            if ("GET".equals(method)) {
                if (path.equals("/patients")) {
                    handleGetAllPatients(exchange);
                } else if (path.matches("/patients/\\d+")) {
                    handleGetPatientById(exchange);
                } else {
                    sendResponse(exchange, "Invalid endpoint", 404);
                }
            }
            // Handle POST requests
            else if ("POST".equals(method)) {
                if (path.equals("/patients")) {
                    handleAddPatient(exchange);
                } else if (path.matches("/patients/\\d+")) {
                    handleUpdatePatient(exchange);
                } else {
                    sendResponse(exchange, "Invalid endpoint", 404);
                }
            }
            else {
                sendResponse(exchange, "Method not allowed", 405);
            }
        } catch (SQLException e) {
            sendResponse(exchange, "Database error: " + e.getMessage(), 500);
        } catch (Exception e) {
            sendResponse(exchange, "Server error: " + e.getMessage(), 500);
        }
    }

    private void handleGetAllPatients(HttpExchange exchange) throws IOException, SQLException {
        List<Patient> patients = DBHelper.getAllPatients();
        String response = gson.toJson(patients);
        sendResponse(exchange, response, 200);
    }

    private void handleGetPatientById(HttpExchange exchange) throws IOException, SQLException {
        String path = exchange.getRequestURI().getPath();
        int id = Integer.parseInt(path.split("/")[2]);
        
        Patient patient = DBHelper.getPatientById(id);
        if (patient != null) {
            String response = gson.toJson(patient);
            sendResponse(exchange, response, 200);
        } else {
            sendResponse(exchange, "Patient not found", 404);
        }
    }

    private void handleAddPatient(HttpExchange exchange) throws IOException, SQLException {
        InputStreamReader isr = new InputStreamReader(exchange.getRequestBody(), StandardCharsets.UTF_8);
        Patient patient = gson.fromJson(isr, Patient.class);
        
        DBHelper.insertPatient(patient);
        sendResponse(exchange, "{\"status\":\"Patient added successfully\"}", 201);
    }

    private void handleUpdatePatient(HttpExchange exchange) throws IOException, SQLException {
        String path = exchange.getRequestURI().getPath();
        int id = Integer.parseInt(path.split("/")[2]);
        
        InputStreamReader isr = new InputStreamReader(exchange.getRequestBody(), StandardCharsets.UTF_8);
        Patient patient = gson.fromJson(isr, Patient.class);
        patient.setId(id);
        
        DBHelper.updatePatient(patient);
        sendResponse(exchange, "{\"status\":\"Patient updated successfully\"}", 200);
    }

    private void sendResponse(HttpExchange exchange, String response, int statusCode) throws IOException {
        exchange.getResponseHeaders().set("Content-Type", "application/json");
        exchange.sendResponseHeaders(statusCode, response.getBytes().length);
        try (OutputStream os = exchange.getResponseBody()) {
            os.write(response.getBytes());
        }
    }
} 