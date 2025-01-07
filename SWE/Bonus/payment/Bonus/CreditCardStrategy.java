
import java.io.*;
import java.util.*;

/**
 * 
 */
public class CreditCardStrategy extends PaymentStrategy implements Interface3 {

    /**
     * Default constructor
     */
    public CreditCardStrategy() {
    }

    /**
     * 
     */
    private void String cardNumber;

    /**
     * 
     */
    private void String cardHolderName;

    /**
     * 
     */
    private void String expirationDate;

    /**
     * 
     */
    private void String cvv;

    /**
     * @param String cardNumber 
     * @param String name 
     * @param String expDate 
     * @param String cvv
     */
    public CreditCardStrategy(void String cardNumber, void String name, void String expDate, void String cvv) {
        // TODO implement here
    }

    /**
     * @param double amount 
     * @return
     */
    public boolean pay(void double amount) {
        // TODO implement here
        return false;
    }

    /**
     * @return
     */
    public boolean validatePayment() {
        // TODO implement here
        return false;
    }

}