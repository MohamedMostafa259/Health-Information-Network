
import java.io.*;
import java.util.*;

/**
 * 
 */
public class DebitCardStrategy implements PaymentStrategy {
    private String cardNumber;
    private String cardHolderName;
    private String bankName;

    public DebitCardStrategy(String cardNumber, String cardHolderName, String bankName) {
        this.cardNumber = cardNumber;
        this.cardHolderName = cardHolderName;
        this.bankName = bankName;
    }

    public boolean pay(double amount) {
        if (validatePayment()) {
            System.out.println("Paying $" + amount + " using Debit Card from " + bankName);
            return true;
        }
        return false;
    }

    /**
     * @return
     */
    public boolean validatePayment() {
        return cardNumber != null && !cardNumber.isEmpty() && 
               cardNumber.length() == 16 && bankName != null;
    }

}