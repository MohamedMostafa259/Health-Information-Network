import java.util.Scanner;
public class ViewFactoryDemo {
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        
        System.out.println("Enter your role (patient, provider, or regulator):");
        String role = scanner.nextLine();
        
        ViewFactory factory;
        if (role.equalsIgnoreCase("patient")) {
            factory = new PatientViewFactory();
        } else if (role.equalsIgnoreCase("provider")) {
            factory = new ProviderViewFactory();
        } else if (role.equalsIgnoreCase("regulator")) {
            factory = new RegulatorViewFactory();
        } else {
            System.out.println("Invalid role: " + role);
            scanner.close();
            return;
        }
        
        Dashboard dashboard = factory.createDashboard();
        Form form = factory.createForm();
        NotificationPanel notificationPanel = factory.createNotificationPanel();
        
        System.out.println("Your UI Components:");
        System.out.println(dashboard.render());
        System.out.println(form.display());
        System.out.println(notificationPanel.showNotifications());
        
        scanner.close();
    }
}
