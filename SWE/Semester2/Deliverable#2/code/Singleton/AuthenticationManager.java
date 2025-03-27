package Singleton;
import java.util.HashMap;
import java.util.Map;

public class AuthenticationManager {
    private static volatile AuthenticationManager instance;
    private Map<String, UserSession> activeSessions;
    
    private AuthenticationManager() {
        activeSessions = new HashMap<>();
    }
    
    public static AuthenticationManager getInstance() {
        AuthenticationManager result = instance;
        if (result == null) {
            synchronized (AuthenticationManager.class) {
                result = instance;
                if (result == null) {
                    result = instance = new AuthenticationManager();
                }
            }
        }
        return result;
    }
    
    public boolean authenticate(String username, String password) {
        return validateCredentials(username, password);
    }
    
    public void createSession(String username) {
        UserSession session = new UserSession(username);
        activeSessions.put(username, session);
    }
    
    public void invalidateSession(String username) {
        activeSessions.remove(username);
    }
    
    private boolean validateCredentials(String username, String password) {
        // validation logic
        return true; 
    }
    
    // session management
    private class UserSession {
        private String username;
        private long createdAt;
        
        public UserSession(String username) {
            this.username = username;
            this.createdAt = System.currentTimeMillis();
        }
    }
}