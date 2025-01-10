
import java.io.*;
import java.util.*;

/**
 * 
 */
public class InsuranceStrategy implements PaymentStrategy {
    private String insuranceId;
    private String policyNumber;
    private double coveragePercentage;

    public InsuranceStrategy(String insuranceId, String policyNumber, double coveragePercentage) {
        this.insuranceId = insuranceId;
        this.policyNumber = policyNumber;
        this.coveragePercentage = coveragePercentage;

    }

    /**
     * @param double amount 
     * @return
     */
    public boolean pay(double amount) {
        if (validatePayment()) {
            double coveredAmount = amount * (coveragePercentage / 100.0);
            System.out.println("Processing insurance payment for $" + coveredAmount);
            return true;
        }
        return false;
    }

    /**
     * @return
     */
    public boolean validatePayment() {
        return insuranceId != null && policyNumber != null && 
               coveragePercentage > 0 && coveragePercentage <= 100;
    }

}