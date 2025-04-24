package com.healthinformationnetwork.patterns.decorator;

// Base interface
public interface MedicalRecord {
    String getContent();
}

// Concrete implementation
class BasicMedicalRecord implements MedicalRecord {
    private String content;

    public BasicMedicalRecord(String content) {
        this.content = content;
    }

    @Override
    public String getContent() {
        return content;
    }
}

// Decorator abstract class
abstract class MedicalRecordDecorator implements MedicalRecord {
    protected MedicalRecord decoratedRecord;

    public MedicalRecordDecorator(MedicalRecord decoratedRecord) {
        this.decoratedRecord = decoratedRecord;
    }

    @Override
    public String getContent() {
        return decoratedRecord.getContent();
    }
}

// Encryption decorator
class EncryptedMedicalRecord extends MedicalRecordDecorator {
    public EncryptedMedicalRecord(MedicalRecord decoratedRecord) {
        super(decoratedRecord);
    }

    @Override
    public String getContent() {
        return encrypt(super.getContent());
    }

    private String encrypt(String content) {
        // Implementation of encryption
        return "ENCRYPTED: " + content;
    }
}

// Compression decorator
class CompressedMedicalRecord extends MedicalRecordDecorator {
    public CompressedMedicalRecord(MedicalRecord decoratedRecord) {
        super(decoratedRecord);
    }

    @Override
    public String getContent() {
        return compress(super.getContent());
    }

    private String compress(String content) {
        // Implementation of compression
        return "COMPRESSED: " + content;
    }
} 