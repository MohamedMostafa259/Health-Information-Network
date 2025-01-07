public class HealthProviderNotification implements NotificationObserver {
    @Override
    public void update(String notification) {
        System.out.println("Health Provider Notification: " + notification);
    }
}