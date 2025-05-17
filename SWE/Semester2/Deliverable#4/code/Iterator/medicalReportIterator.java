package SWE.Semester2.Deliverable4.code.Iterator;

import java.util.List;
import java.util.ArrayList;

// Iterator Interface
interface MedicalReportIterator {
    boolean hasNext();
    MedicalReport next();
    void reset();
}

// Aggregate Interface
interface MedicalReportCollection {
    MedicalReportIterator createIterator();
    void addReport(MedicalReport report);
    int getSize();
}

// Concrete Aggregate
class PatientMedicalReports implements MedicalReportCollection {
    private List<MedicalReport> reports;

    public PatientMedicalReports() {
        this.reports = new ArrayList<>();
    }

    public MedicalReportIterator createIterator() {
        return new PatientReportIterator(this);
    }
    
    public void addReport(MedicalReport report) {
        reports.add(report);
    }

    public int getSize() {
        return reports.size();
    }

    public MedicalReport getReport(int index) {
        return reports.get(index);
    }
}

// Concrete Iterator
class PatientReportIterator implements MedicalReportIterator {
    private PatientMedicalReports reports;
    private int currentPosition;

    public PatientReportIterator(PatientMedicalReports reports) {
        this.reports = reports;
        this.currentPosition = 0;
    }
    
    public boolean hasNext() {
        return currentPosition < reports.getSize();
    }
    
    public MedicalReport next() {
        if (hasNext()) {
            return reports.getReport(currentPosition++);
        }
        return null;
    }
    
    public void reset() {
        currentPosition = 0;
    }
}

// Medical Report class
class MedicalReport {
    private String reportId;
    private String patientId;
    private String diagnosis;
    private String date;

    public MedicalReport(String reportId, String patientId, String diagnosis, String date) {
        this.reportId = reportId;
        this.patientId = patientId;
        this.diagnosis = diagnosis;
        this.date = date;
    }

    
    public String toString() {
        return "Report ID: " + reportId + 
               "\nPatient ID: " + patientId + 
               "\nDiagnosis: " + diagnosis + 
               "\nDate: " + date + "\n";
    }
}

// Client 
public class Client {
    public static void main(String[] args) {
        MedicalReportCollection reports = new PatientMedicalReports();

        // Add some medical reports
        reports.addReport(new MedicalReport("R001", "P123", "Regular checkup - All normal", "2024-03-15"));
        reports.addReport(new MedicalReport("R002", "P123", "Blood test results - Normal", "2024-03-20"));
        reports.addReport(new MedicalReport("R003", "P123", "X-ray examination - Clear", "2024-03-25"));

        MedicalReportIterator iterator = reports.createIterator();

        // Iterate through reports
        System.out.println("Iterating through medical reports:");
        System.out.println("--------------------------------");
        while (iterator.hasNext()) {
            MedicalReport report = iterator.next();
            System.out.println(report);
        }

        // Reset iterator and iterate again
        System.out.println("\nResetting and iterating again:");
        System.out.println("--------------------------------");
        iterator.reset();
        while (iterator.hasNext()) {
            MedicalReport report = iterator.next();
            System.out.println(report);
        }
    }
}

