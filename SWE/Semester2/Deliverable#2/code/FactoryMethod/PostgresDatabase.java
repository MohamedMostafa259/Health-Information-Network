package FactoryMethod;

public class PostgresDatabase extends DatabaseConnectionFactory {
    @Override
    public DatabaseConnection getConnection() {
        return new PostgreSQLConnection();
    }
}
