import java.time.LocalDateTime;

public class Patient {
    private String patientId;
    private String name;
    private Payment currentPayment;

    public Patient(String patientId, String name) {
        this.patientId = patientId;
        this.name = name;
    }

    public void makePayment(double amount) {
        this.currentPayment = new Payment(amount, generatePaymentId());
    }

    public void processPayment(PaymentStrategy strategy) {
        if (currentPayment != null) {
            currentPayment.setPaymentStrategy(strategy);
            currentPayment.processPayment();
        } else {
            throw new IllegalStateException("No payment initialized. Call makePayment first.");
        }
    }

    private String generatePaymentId() {
        return "PAY-" + patientId + "-" + System.currentTimeMillis();
    }
}

// Payment Strategy Interface
public interface PaymentStrategy {
    boolean pay(double amount);
    boolean validatePayment();
}

// Concrete strategy for credit card payments
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

    @Override
    public boolean pay(double amount) {
        if (validatePayment()) {
            System.out.println("Paying $" + amount + " using Credit Card");
            return true;
        }
        return false;
    }

    @Override
    public boolean validatePayment() {
        // Add credit card validation logic
        return cardNumber != null && !cardNumber.isEmpty() && 
               cardNumber.length() == 16 && cvv.length() == 3;
    }
}

// Concrete strategy for insurance payments
public class InsuranceStrategy implements PaymentStrategy {
    private String insuranceId;
    private String policyNumber;
    private double coveragePercentage;

    public InsuranceStrategy(String insuranceId, String policyNumber, double coveragePercentage) {
        this.insuranceId = insuranceId;
        this.policyNumber = policyNumber;
        this.coveragePercentage = coveragePercentage;
    }

    @Override
    public boolean pay(double amount) {
        if (validatePayment()) {
            double coveredAmount = amount * (coveragePercentage / 100.0);
            System.out.println("Processing insurance payment for $" + coveredAmount);
            return true;
        }
        return false;
    }

    @Override
    public boolean validatePayment() {
        return insuranceId != null && policyNumber != null && 
               coveragePercentage > 0 && coveragePercentage <= 100;
    }
}

// Concrete strategy for debit card payments
public class DebitCardStrategy implements PaymentStrategy {
    private String cardNumber;
    private String cardHolderName;
    private String bankName;

    public DebitCardStrategy(String cardNumber, String cardHolderName, String bankName) {
        this.cardNumber = cardNumber;
        this.cardHolderName = cardHolderName;
        this.bankName = bankName;
    }

    @Override
    public boolean pay(double amount) {
        if (validatePayment()) {
            System.out.println("Paying $" + amount + " using Debit Card from " + bankName);
            return true;
        }
        return false;
    }

    @Override
    public boolean validatePayment() {
        return cardNumber != null && !cardNumber.isEmpty() && 
               cardNumber.length() == 16 && bankName != null;
    }
}

// Context class
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

    public void setPaymentStrategy(PaymentStrategy strategy) {
        this.paymentStrategy = strategy;
    }

    public boolean processPayment() {
        if (paymentStrategy == null) {
            throw new IllegalStateException("Payment strategy not set");
        }
        return paymentStrategy.pay(amount);
    }
}

// Example 
public class PaymentDemo {
    public static void main(String[] args) {
        // Create payment
        Payment payment = new Payment(100.0, "PAY123");

        // Process with credit card
        payment.setPaymentStrategy(new CreditCardStrategy(
            "1234567890123456", "Mohamed Ibrahim", "12/25", "123"));
        payment.processPayment();

        // Process with insurance
        payment.setPaymentStrategy(new InsuranceStrategy(
            "INS001", "POL123", 80.0));
        payment.processPayment();

        // Process with debit card
        payment.setPaymentStrategy(new DebitCardStrategy(
            "9876543210987654", "Mohamed Mostafa", "CIB"));
        payment.processPayment();
    }
}