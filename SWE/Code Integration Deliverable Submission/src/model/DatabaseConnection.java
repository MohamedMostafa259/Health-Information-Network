package model;

import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.SQLException;

public class DatabaseConnection {
    // private static final String URL = "jdbc:sqlserver://localhost:1433;" +
    // "instanceName=SQLEXPRESS;" +
    // "databaseName=HIN;" +
    // "trustServerCertificate=true;" +
    // "integratedSecurity=true;" +
    // "loginTimeout=30;" +
    // "encrypt=true;";
    
    // private static final String URL = "jdbc:sqlserver://localhost\\SQLEXPRESS:1433;databaseName=HIN;encrypt=false;" + 
    // "trustServerCertificate=false";
    // private static final String USER = "Mohamed_Mostafa\\Mohamed";
    // private static final String PASSWORD = "1234";
    private static final String URL = "jdbc:sqlserver://localhost:1433;databaseName=HIN;trustServerCertificate=true;encrypt=false";

    // private static final String URL = "jdbc:sqlserver://localhost:1433;instanceName=SQLEXPRESS;databaseName=HIN;trustServerCertificate=true;integratedSecurity=true;";
    // private static final String URL = "jdbc:sqlserver://Mohamed_Mostafa\\SQLEXPRESS;databaseName=HIN;integratedSecurity=true;";
    // private static final String URL = "jdbc:sqlserver://Mohamed_Mostafa\\SQLEXPRESS;Database=HIN;integratedSecurity=true";
    private static Connection connection = null;

    static {
        try {
            Class.forName("com.microsoft.sqlserver.jdbc.SQLServerDriver");
        } catch (ClassNotFoundException e) {
            e.printStackTrace();
        }
    }

    // private static final String URL = "jdbc:sqlserver://localhost:1433;instanceName=SQLEXPRESS;databaseName=HIN;trustServerCertificate=true;";
    // private static final String USER = "your_username";
    // private static final String PASSWORD = "your_password";
    
    // public static Connection getConnection() {
    //     if (connection == null) {
    //         try {
    //             connection = DriverManager.getConnection(URL, USER, PASSWORD);
    //         } catch (SQLException e) {
    //             e.printStackTrace();
    //         }
    //     }
    //     return connection;
    // }

    public static Connection getConnection() {
        if (connection == null) {
            try {
                connection = DriverManager.getConnection(URL);
                System.out.println("connection established");

            } catch (SQLException e) {
                System.out.println("error connecting to the database");
                e.printStackTrace();
            }
        }
        return connection;
    }

    public static void closeConnection() {
        if (connection != null) {
            try {
                connection.close();
            } catch (SQLException e) {
                e.printStackTrace();
            }
        }
    }
}