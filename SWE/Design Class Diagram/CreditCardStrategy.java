
import java.io.*;
import java.util.*;

/**
 * 
 */
public class CreditCardStrategy implements PaymentStrategy {
    private String cardNumber;
    private String cardHolderName;
    private String expirationDate;
    private String cvv;

    public CreditCardStrategy(String cardNumber, String cardHolderName, 
    String expirationDate, String cvv) {
        this.cardNumber = cardNumber;
        this.cardHolderName = cardHolderName;
        this.expirationDate = expirationDate;
        this.cvv = cvv;
    }


    /**
     * @param String cardNumber 
     * @param String name 
     * @param String expDate 
     * @param String cvv
     */


    /**
     * @param double amount 
     * @return
     */
    public boolean pay(double amount) {
        if (validatePayment()) {
            System.out.println("Paying $" + amount + " using Credit Card");
            return true;
        }
        return false;
    }

    /**
     * @return
     */
    public boolean validatePayment() {
        // Add credit card validation logic
        return cardNumber != null && !cardNumber.isEmpty() && 
               cardNumber.length() == 16 && cvv.length() == 3;
    }

}