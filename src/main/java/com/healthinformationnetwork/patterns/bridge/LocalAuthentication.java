package com.healthinformationnetwork.patterns.bridge;

import java.util.HashMap;
import java.util.Map;

public class LocalAuthentication implements AuthenticationMethod {
    private Map<String, String> userCredentials;
    private Map<String, Boolean> authenticatedUsers;

    public LocalAuthentication() {
        this.userCredentials = new HashMap<>();
        this.authenticatedUsers = new HashMap<>();
    }

    @Override
    public boolean authenticate(String username, String credentials) {
        if (userCredentials.containsKey(username) && 
            userCredentials.get(username).equals(credentials)) {
            authenticatedUsers.put(username, true);
            return true;
        }
        return false;
    }

    @Override
    public void logout(String username) {
        authenticatedUsers.remove(username);
    }

    @Override
    public boolean isAuthenticated(String username) {
        return authenticatedUsers.getOrDefault(username, false);
    }

    // Method to register new users (for demonstration)
    public void registerUser(String username, String credentials) {
        userCredentials.put(username, credentials);
    }
} 