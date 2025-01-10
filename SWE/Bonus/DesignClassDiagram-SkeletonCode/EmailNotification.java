public class EmailNotification implements NotificationObserver {
    @Override
    public void update(String notification) {
        System.out.println("Email Notification: " + notification);
    }
}