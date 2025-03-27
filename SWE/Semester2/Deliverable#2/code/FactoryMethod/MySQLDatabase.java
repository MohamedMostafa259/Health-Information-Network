package FactoryMethod;

public class MySQLDatabase extends DatabaseConnectionFactory {
    @Override
    public DatabaseConnection getConnection() {
        return new MySQLConnection();
    }
}
