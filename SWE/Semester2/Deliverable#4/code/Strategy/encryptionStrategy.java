package SWE.Semester2.Deliverable#4.code.Strategy;

interface EncryptionStrategy {
    void encrypt(String data);
}

class AESEncryption implements EncryptionStrategy {
    public void encrypt(String data) {
        System.out.println("Encrypting with AES: " + data);
    }
}

class RSAEncryption implements EncryptionStrategy {
    public void encrypt(String data) {
        System.out.println("Encrypting with RSA: " + data);
    }
}

class SecureDataSender {
    private EncryptionStrategy strategy;

    public void setStrategy(EncryptionStrategy s) {
        this.strategy = s;
    }

    public void send(String data) {
        strategy.encrypt(data);
    }
}
