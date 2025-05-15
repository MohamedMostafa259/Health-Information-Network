package SWE.Semester2.Deliverable#4.code.Strategy;

interface BillingStrategy {
    void calculateBill();
}

class PrivateInsuranceBilling implements BillingStrategy {
    public void calculateBill() {
        System.out.println("Private insurance billing applied.");
    }
}

class GovernmentInsuranceBilling implements BillingStrategy {
    public void calculateBill() {
        System.out.println("Government insurance billing applied.");
    }
}

class BillingProcessor {
    private BillingStrategy strategy;

    public void setStrategy(BillingStrategy s) {
        this.strategy = s;
    }

    public void process() {
        strategy.calculateBill();
    }
}
