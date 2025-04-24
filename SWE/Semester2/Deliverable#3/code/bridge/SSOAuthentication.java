package com.healthinformationnetwork.patterns.bridge;

import java.util.HashMap;
import java.util.Map;

public class SSOAuthentication implements AuthenticationMethod {
    private Map<String, String> ssoTokens;
    private Map<String, Boolean> authenticatedUsers;

    public SSOAuthentication() {
        this.ssoTokens = new HashMap<>();
        this.authenticatedUsers = new HashMap<>();
    }

    @Override
    public boolean authenticate(String username, String token) {
        // Validate SSO token (simplified implementation)
        if (isValidToken(token)) {
            ssoTokens.put(username, token);
            authenticatedUsers.put(username, true);
            return true;
        }
        return false;
    }

    @Override
    public void logout(String username) {
        ssoTokens.remove(username);
        authenticatedUsers.remove(username);
    }

    @Override
    public boolean isAuthenticated(String username) {
        return authenticatedUsers.getOrDefault(username, false);
    }

    private boolean isValidToken(String token) {
        // Simplified token validation logic
        return token != null && !token.isEmpty() && token.startsWith("SSO_");
    }

    // Method to get the SSO token for a user
    public String getToken(String username) {
        return ssoTokens.get(username);
    }
} 