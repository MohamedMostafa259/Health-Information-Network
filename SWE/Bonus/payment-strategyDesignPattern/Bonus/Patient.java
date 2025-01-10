
import java.io.*;
import java.util.*;

/**
 * 
 */
public class Patient {
    private String patientId;
    private String name;
    private Payment currentPayment;

    public Patient(String patientId, String name) {
        this.patientId = patientId;
        this.name = name;
    }

    /**
     * @param String patientId 
     * @param String name
     */

    /**
     * @param double amount 
     * @return
     */
    public void makePayment(double amount) {
        this.currentPayment = new Payment(amount, generatePaymentId());
    }


    /**
     * @param PaymentStrategy strategy 
     * @return
     */
    
     public void processPayment(PaymentStrategy strategy) {
        if (currentPayment != null) {
            currentPayment.setPaymentStrategy(strategy);
            currentPayment.processPayment();
        } else {
            throw new IllegalStateException("No payment initialized. Call makePayment first.");
        }
    }


    /**
     * @return
     */
    private String generatePaymentId() {
        return "PAY-" + patientId + "-" + System.currentTimeMillis();
    }

}

