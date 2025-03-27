
import java.io.*;
import java.time.LocalDateTime;
import java.util.*;

/**
 * 
 */
public class Payment {
 private double amount;
    private String paymentId;
    private LocalDateTime paymentDate;
    private PaymentStrategy paymentStrategy;

    public Payment(double amount, String paymentId) {
        this.amount = amount;
        this.paymentId = paymentId;
        this.paymentDate = LocalDateTime.now();
    }



    /**
     * @param double amount 
     * @param String paymentId
     */
 

    /**
     * @return
     */
    public boolean processPayment() {
      if (paymentStrategy == null) {
            throw new IllegalStateException("Payment strategy not set");
        }
        return paymentStrategy.pay(amount);
    }
    

    /**
     * @param PaymentStrategy strategy 
     * @return
     */
    public void setPaymentStrategy(PaymentStrategy strategy) {
        this.paymentStrategy = strategy;

    }
}