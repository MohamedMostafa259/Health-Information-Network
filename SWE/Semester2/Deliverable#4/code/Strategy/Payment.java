/* IDEA:
The PaymentStrategy pattern enables a health information system to support 
multiple payment methods (like credit card, insurance, mobile wallet, etc.) 
in a flexible and maintainable way. As a result, the system now can switch 
between payment methods at runtime without changing core logic. 
This approach makes it easy to add new payment options, 
and ensures the system can adapt to future payment technologies.
*/

import java.util.*;

// Strategy Interface
interface PaymentStrategy {
    boolean pay(double amount);
    boolean validatePayment();
}

// Concrete Strategy: Credit Card
class CreditCardStrategy implements PaymentStrategy {
    private String cardNumber, cardHolder, expDate, cvv;
    public CreditCardStrategy(String cardNumber, String cardHolder, String expDate, String cvv) {
        this.cardNumber = cardNumber;
        this.cardHolder = cardHolder;
        this.expDate = expDate;
        this.cvv = cvv;
    }
    public boolean pay(double amount) {
        if (validatePayment()) {
            return true;
        }
        return false;
    }
    public boolean validatePayment() {
        return cardNumber.length() == 16 && cvv.length() == 3;
    }
}

// Concrete Strategy: Insurance
class InsuranceStrategy implements PaymentStrategy {
    private String insuranceId, policyNumber;
    private double coveragePercent;
    public InsuranceStrategy(String insuranceId, String policyNumber, double coveragePercent) {
        this.insuranceId = insuranceId;
        this.policyNumber = policyNumber;
        this.coveragePercent = coveragePercent;
    }
    public boolean pay(double amount) {
        if (validatePayment()) {
            return true;
        }
        return false;
    }
    public boolean validatePayment() {
        return coveragePercent > 0 && coveragePercent <= 100;
    }
}

// Context
class Payment {
    private double amount;
    private PaymentStrategy strategy;
    public Payment(double amount) { this.amount = amount; }
    public void setPaymentStrategy(PaymentStrategy strategy) { this.strategy = strategy; }
    public boolean processPayment() {
        return strategy.pay(amount);
    }
}

// Client
public class Client {
    public static void main(String[] args) {
        Payment payment = new Payment(200.0);

        PaymentStrategy creditCard = new CreditCardStrategy("1234567812345678", "John Doe", "12/26", "123");
        payment.setPaymentStrategy(creditCard);
        payment.processPayment();

        PaymentStrategy insurance = new InsuranceStrategy("INS-001", "POL-123", 80.0);
        payment.setPaymentStrategy(insurance);
        payment.processPayment();
    }
}