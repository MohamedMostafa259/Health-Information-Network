package SWE.Semester2.Deliverable4.code.Iterator;

public class PatientRecordIterator implements Iterator {
    private PatientRecordCollection collection;
    private int index = 0;

    public PatientRecordIterator(PatientRecordCollection collection) {
        this.collection = collection;
    }

    @Override
    public boolean hasNext() {
        return index < collection.size();
    }

    @Override
    public PatientRecord next() {
        return collection.get(index++);
    }
}
