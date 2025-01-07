public class PhoneNotification implements NotificationObserver {
    @Override
    public void update(String notification) {
        System.out.println("Phone Notification: " + notification);
    }
}