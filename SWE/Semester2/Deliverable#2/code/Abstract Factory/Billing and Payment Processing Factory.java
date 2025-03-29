// Abstract Factory Interface
interface PaymentProcessingFactory {
    PaymentValidator createValidator();
    TransactionHandler createTransactionHandler();
    ReceiptGenerator createReceiptGenerator();
}

// Abstract Product Interfaces
interface PaymentValidator {
    boolean validate(String paymentDetails);
}

interface TransactionHandler {
    boolean processTransaction(double amount);
}

interface ReceiptGenerator {
    String generateReceipt(double amount);
}

// Concrete Products for Credit Card
class CreditCardValidator implements PaymentValidator {
    @Override
    public boolean validate(String paymentDetails) {
        return paymentDetails != null && !paymentDetails.isEmpty();
    }
}

class CreditCardTransactionHandler implements TransactionHandler {
    @Override
    public boolean processTransaction(double amount) {
        return true;
    }
}

class CreditCardReceiptGenerator implements ReceiptGenerator {
    @Override
    public String generateReceipt(double amount) {
        return "Credit Card Payment Receipt: Amount paid $" + amount;
    }
}

// Concrete Products for Bank Transfer
class BankTransferValidator implements PaymentValidator {
    @Override
    public boolean validate(String paymentDetails) {
        return paymentDetails != null && !paymentDetails.isEmpty();
    }
}

class BankTransferTransactionHandler implements TransactionHandler {
    @Override
    public boolean processTransaction(double amount) {
        return true;
    }
}

class BankTransferReceiptGenerator implements ReceiptGenerator {
    @Override
    public String generateReceipt(double amount) {
        return "Bank Transfer Receipt: Amount transferred $" + amount;
    }
}

// Concrete Factories
class CreditCardPaymentFactory implements PaymentProcessingFactory {
    @Override
    public PaymentValidator createValidator() {
        return new CreditCardValidator();
    }

    @Override
    public TransactionHandler createTransactionHandler() {
        return new CreditCardTransactionHandler();
    }

    @Override
    public ReceiptGenerator createReceiptGenerator() {
        return new CreditCardReceiptGenerator();
    }
}

class BankTransferPaymentFactory implements PaymentProcessingFactory {
    @Override
    public PaymentValidator createValidator() {
        return new BankTransferValidator();
    }

    @Override
    public TransactionHandler createTransactionHandler() {
        return new BankTransferTransactionHandler();
    }

    @Override
    public ReceiptGenerator createReceiptGenerator() {
        return new BankTransferReceiptGenerator();
    }
}

