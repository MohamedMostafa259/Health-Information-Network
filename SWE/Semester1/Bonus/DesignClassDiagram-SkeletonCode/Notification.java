import java.util.ArrayList;
import java.util.List;

public class Notification implements NotificationService {
    private List<NotificationObserver> observers = new ArrayList<>();
    private List<String> patients = new ArrayList<>();
    private String notification;

    public void addPatient(String patient) {
        patients.add(patient);
        notification = "New patient added: " + patient;
        notifyObservers();
    }

    public void removePatient(String patient) {
        patients.remove(patient);
        notification = "Patient removed: " + patient;
        notifyObservers();
    }

    public void notifyPatient(String message) {
        notification = message;
        notifyObservers();
    }

    @Override
    public void addObserver(NotificationObserver observer) {
        observers.add(observer);
    }

    @Override
    public void removeObserver(NotificationObserver observer) {
        observers.remove(observer);
    }

    @Override
    public void notifyObservers() {
        for (NotificationObserver observer : observers) {
            observer.update(notification);
        }
    }
}