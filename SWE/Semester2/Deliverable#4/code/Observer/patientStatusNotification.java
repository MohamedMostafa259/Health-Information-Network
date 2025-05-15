package SWE.Semester2.Deliverable#4.code.Observer;

public class patientStatusNotification {

    interface Observer {
        void update(String status);
    }

    interface Subject {
        void addObserver(Observer o);
        void removeObserver(Observer o);
        void notifyObservers();
    }

    static class Patient implements Subject {
        private final java.util.List<Observer> observers = new java.util.ArrayList<>();
        private String status;

        public void addObserver(Observer o) {
            observers.add(o);
        }

        public void removeObserver(Observer o) {
            observers.remove(o);
        }

        public void notifyObservers() {
            for (Observer o : observers) {
                o.update(status);
            }
        }

        public void setStatus(String status) {
            this.status = status;
            notifyObservers();
        }
    }

    static class Doctor implements Observer {
        public void update(String status) {
            System.out.println("Doctor notified: Patient status is " + status);
        }
    }

    static class FamilyMember implements Observer {
        public void update(String status) {
            System.out.println("Family member notified: Patient status is " + status);
        }
    }

   
    public static void main(String[] args) {
        Patient patient = new Patient();

        Observer doctor = new Doctor();
        Observer family = new FamilyMember();

        patient.addObserver(doctor);
        patient.addObserver(family);

        patient.setStatus("Stable");
        patient.setStatus("Critical");
    }
}
