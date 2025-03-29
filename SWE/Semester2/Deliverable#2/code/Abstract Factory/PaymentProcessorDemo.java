import java.util.Scanner;

public class PaymentProcessorDemo {
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        
        System.out.println("Enter payment method (credit card or bank transfer):");
        String paymentMethod = scanner.nextLine();
        
        System.out.println("Enter payment details (e.g., card number or bank account):");
        String paymentDetails = scanner.nextLine();
        
        System.out.println("Enter amount:");
        double amount = scanner.nextDouble();
        
        processPayment(paymentMethod, paymentDetails, amount);
        
        scanner.close();
    }

    private static void processPayment(String paymentMethod, String paymentDetails, double amount) {
        PaymentProcessingFactory factory;
        if (paymentMethod.equalsIgnoreCase("credit card")) {
            factory = new CreditCardPaymentFactory();
        } else if (paymentMethod.equalsIgnoreCase("bank transfer")) {
            factory = new BankTransferPaymentFactory();
        } else {
            System.out.println("Unsupported payment method: " + paymentMethod);
            return;
        }

        PaymentValidator validator = factory.createValidator();
        if (validator.validate(paymentDetails)) {
            TransactionHandler handler = factory.createTransactionHandler();
            if (handler.processTransaction(amount)) {
                ReceiptGenerator receiptGen = factory.createReceiptGenerator();
                String receipt = receiptGen.generateReceipt(amount);
                System.out.println(receipt);
            } else {
                System.out.println("Transaction failed.");
            }
        } else {
            System.out.println("Invalid payment details.");
        }
    }
}

