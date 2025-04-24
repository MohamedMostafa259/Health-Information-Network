package com.healthinformationnetwork.patterns.decorator;

public class AccessControlDecorator extends MedicalRecordDecorator {
    private String userRole;

    public AccessControlDecorator(MedicalRecord decoratedRecord, String userRole) {
        super(decoratedRecord);
        this.userRole = userRole;
    }

    @Override
    public String getContent() {
        if (hasAccess()) {
            return super.getContent();
        }
        return "Access Denied: Insufficient privileges";
    }

    private boolean hasAccess() {
        // Simplified access control logic
        return "DOCTOR".equals(userRole) || "ADMIN".equals(userRole);
    }

    public void setUserRole(String userRole) {
        this.userRole = userRole;
    }

    public String getUserRole() {
        return userRole;
    }
} 