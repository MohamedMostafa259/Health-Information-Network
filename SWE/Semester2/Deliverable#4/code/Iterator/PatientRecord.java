package SWE.Semester2.Deliverable4.code.Iterator;
public class PatientRecord {
    private String id;
    private String name;
    private String diagnosis;

    public PatientRecord(String id, String name, String diagnosis) {
        this.id = id;
        this.name = name;
        this.diagnosis = diagnosis;
    }

    public String getDetails() {
        return "ID: " + id + ", Name: " + name + ", Diagnosis: " + diagnosis;
    }

}
