package FactoryMethod;
import java.sql.Connection;

public interface DatabaseConnection {
    Connection connect();
}