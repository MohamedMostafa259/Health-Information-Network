package com.healthinformationnetwork.patterns.bridge;

public interface AuthenticationMethod {
    boolean authenticate(String username, String credentials);
    void logout(String username);
    boolean isAuthenticated(String username);
} 