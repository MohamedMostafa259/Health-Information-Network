package FactoryMethod;
import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.SQLException;

public class PostgreSQLConnection implements DatabaseConnection {
    @Override
    public Connection connect() {
        try {
            return DriverManager.getConnection("jdbc:postgresql://localhost:5432/HIN", "root", "1234");
        } catch (SQLException e) {
            throw new RuntimeException("Error connecting to PostgreSQL", e);
        }
    }
}
