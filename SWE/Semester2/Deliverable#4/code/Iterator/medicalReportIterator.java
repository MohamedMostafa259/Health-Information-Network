package SWE.Semester2.Deliverable#4.code.Iterator;

import java.util.List;

interface Iterator<T> {
    boolean hasNext();
    T next();
}

class MedicalRecord {
    String info;
    MedicalRecord(String info) { this.info = info; }
    public String toString() { return info; }
}

class MedicalRecordIterator implements Iterator<MedicalRecord> {
    private List<MedicalRecord> records;
    private int position = 0;

    MedicalRecordIterator(List<MedicalRecord> records) {
        this.records = records;
    }

    public boolean hasNext() {
        return position < records.size();
    }

    public MedicalRecord next() {
        return records.get(position++);
    }
}

class PatientMedicalRecords {
    List<MedicalRecord> records;

    PatientMedicalRecords(List<MedicalRecord> records) {
        this.records = records;
    }

    public Iterator<MedicalRecord> createIterator() {
        return new MedicalRecordIterator(records);
    }
}

