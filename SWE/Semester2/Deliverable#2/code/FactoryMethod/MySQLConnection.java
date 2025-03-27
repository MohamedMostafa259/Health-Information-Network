package FactoryMethod;
import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.SQLException;

public class MySQLConnection implements DatabaseConnection {
    @Override
    public Connection connect() {
        try {
            return DriverManager.getConnection("jdbc:mysql://localhost:3306/dbname", "user", "password");
        } catch (SQLException e) {
            throw new RuntimeException("Error connecting to MySQL", e);
        }
    }
}
