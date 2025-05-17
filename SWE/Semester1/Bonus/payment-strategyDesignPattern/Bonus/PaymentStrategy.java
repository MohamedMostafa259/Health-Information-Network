import java.io.*;
import java.util.*;

public interface PaymentStrategy {
    boolean pay(double amount);
    boolean validatePayment();
}
