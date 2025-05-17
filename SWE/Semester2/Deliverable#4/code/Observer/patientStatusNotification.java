package SWE.Semester2.Deliverable4.code.Observer;

import java.util.ArrayList;
import java.util.List;

// Observer Interface
interface PatientObserver {
    void update(String patientId, String status);
}

// Subject Interface
interface PatientSubject {
    void registerObserver(PatientObserver observer);
    void removeObserver(PatientObserver observer);
    void notifyObservers();
}

// Concrete Subject
class Patient implements PatientSubject {
    private String patientId;
    private String status;
    private List<PatientObserver> observers;

    public Patient(String patientId) {
        this.patientId = patientId;
        this.observers = new ArrayList<>();
    }

    public void registerObserver(PatientObserver observer) {
        observers.add(observer);
    }
    
    public void removeObserver(PatientObserver observer) {
        observers.remove(observer);
    }
    
    public void notifyObservers() {
        for (PatientObserver observer : observers) {
            observer.update(patientId, status);
        }
    }

    public void setStatus(String status) {
        this.status = status;
        notifyObservers();
    }
}

// Concrete Observer
class Doctor implements PatientObserver {
    private String doctorId;

    public Doctor(String doctorId) {
        this.doctorId = doctorId;
    }

    public void update(String patientId, String status) {
        System.out.println("Doctor " + doctorId + " notified: Patient " + patientId + " status is " + status);
    }
}

// Concrete Observer
class FamilyMember implements PatientObserver {
    private String memberName;

    public FamilyMember(String memberName) {
        this.memberName = memberName;
    }

    
    public void update(String patientId, String status) {
        System.out.println("Family member " + memberName + " notified: Patient " + patientId + " status is " + status);
    }
}

// Client 
public class Client {
    public static void main(String[] args) {
        Patient patient = new Patient("P123");

        PatientObserver doctor = new Doctor("D456");
        PatientObserver familyMember = new FamilyMember("John Smith");

        patient.registerObserver(doctor);
        patient.registerObserver(familyMember);

        patient.setStatus("Stable");
        System.out.println("\n--- Status Change ---\n");
        patient.setStatus("Critical");
    }
}
