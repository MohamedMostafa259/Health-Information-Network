package com.healthinformationnetwork.patterns.adapter;

public class LegacySystemAdapter implements ModernHealthcareSystem {
    private LegacyHealthcareSystem legacySystem;

    public LegacySystemAdapter(LegacyHealthcareSystem legacySystem) {
        this.legacySystem = legacySystem;
    }

    @Override
    public String getPatientInfo(String patientId) {
        // Convert legacy system response to modern format
        String legacyData = legacySystem.fetchPatientData(patientId);
        return convertToModernFormat(legacyData);
    }

    private String convertToModernFormat(String legacyData) {
        // Implementation of conversion logic
        return "Converted modern format: " + legacyData;
    }
}

// Legacy system interface
interface LegacyHealthcareSystem {
    String fetchPatientData(String patientId);
}

// Modern system interface
interface ModernHealthcareSystem {
    String getPatientInfo(String patientId);
} 