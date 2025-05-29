package SWE.Semester2.Deliverable4.code.Iterator;

public class Main {
    public static void main(String[] args) {
        PatientRecordCollection records = new PatientRecordCollection();
        records.addRecord(new PatientRecord("001", "John Doe", "Flu"));
        records.addRecord(new PatientRecord("002", "Jane Smith", "Diabetes"));

        Iterator iterator = records.createIterator();

        while (iterator.hasNext()) {
            PatientRecord record = iterator.next();
            System.out.println(record.getDetails());
        }
    }
}
