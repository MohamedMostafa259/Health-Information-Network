package SWE.Semester2.Deliverable4.code.Iterator;

import java.util.ArrayList;
import java.util.List;

public class PatientRecordCollection implements Aggregate {
    private List<PatientRecord> records = new ArrayList<>();

    public void addRecord(PatientRecord record) {
        records.add(record);
    }

    public PatientRecord get(int index) {
        return records.get(index);
    }

    public int size() {
        return records.size();
    }

    @Override
    public Iterator createIterator() {
        return new PatientRecordIterator(this);
    }
}
