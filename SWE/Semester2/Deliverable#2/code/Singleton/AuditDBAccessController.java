package Singleton;
import FactoryMethod.*;
import java.sql.Connection;
import java.sql.SQLException;

public class AuditDBAccessController {
    private static volatile AuditDBAccessController instance;
    private Connection dbConnection;
    
    private AuditDBAccessController() {
        initializeDatabaseConnection();
    }
    
    public static AuditDBAccessController getInstance() {
        AuditDBAccessController result = instance;
        if (result == null) {
            synchronized (AuditDBAccessController.class) {
                result = instance;
                if (result == null) {
                    result = instance = new AuditDBAccessController();
                }
            }
        }
        return result;
    }
    
    private void initializeDatabaseConnection() {
        try {
            DatabaseConnectionFactory mysqlFactory = new MySQLDatabase();
            DatabaseConnection mysqlConnection = mysqlFactory.getConnection();
            dbConnection = mysqlConnection.connect();
        } catch (Exception e) {
            System.err.println("Failed to establish database connection: " + e.getMessage());
        }
    }

    public void closeConnection() {
        // handle SQLException
        try {
            if (dbConnection != null && !dbConnection.isClosed()) {
                dbConnection.close();
            }
        } catch (SQLException e) {
            System.err.println("Error closing database connection");
        }
    }
}