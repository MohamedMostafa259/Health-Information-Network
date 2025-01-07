
import java.io.*;
import java.util.*;

/**
 * 
 */
public class DebitCardStrategy extends PaymentStrategy {

    /**
     * Default constructor
     */
    public DebitCardStrategy() {
    }

    /**
     * 
     */
    public void String cardNumber;

    /**
     * 
     */
    public void String cardHolderName;

    /**
     * 
     */
    public void String bankName;

    /**
     * @param String cardNumber 
     * @param String name 
     * @param String bank
     */
    public DebitCardStrategy(void String cardNumber, void String name, void String bank) {
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