// Abstract Factory Interface
interface ViewFactory {
    Dashboard createDashboard();
    Form createForm();
    NotificationPanel createNotificationPanel();
}

// Abstract Product Interfaces
interface Dashboard {
    String render();
}

interface Form {
    String display();
}

interface NotificationPanel {
    String showNotifications();
}

// Concrete Products for Patient
class PatientDashboard implements Dashboard {
    @Override
    public String render() {
        return "Rendering Patient Dashboard: Displays medical history and upcoming appointments.";
    }
}

class PatientForm implements Form {
    @Override
    public String display() {
        return "Displaying Patient Form: Fields for updating personal and medical information.";
    }
}

class PatientNotificationPanel implements NotificationPanel {
    @Override
    public String showNotifications() {
        return "Showing Patient Notifications: Appointment reminders and health alerts.";
    }
}

// Concrete Products for Provider
class ProviderDashboard implements Dashboard {
    @Override
    public String render() {
        return "Rendering Provider Dashboard: Shows patient appointments and medical records.";
    }
}

class ProviderForm implements Form {
    @Override
    public String display() {
        return "Displaying Provider Form: Fields for adding or updating medical records.";
    }
}

class ProviderNotificationPanel implements NotificationPanel {
    @Override
    public String showNotifications() {
        return "Showing Provider Notifications: New appointments and patient updates.";
    }
}

// Concrete Products for Regulator
class RegulatorDashboard implements Dashboard {
    @Override
    public String render() {
        return "Rendering Regulator Dashboard: Displays compliance metrics and usage analytics.";
    }
}

class RegulatorForm implements Form {
    @Override
    public String display() {
        return "Displaying Regulator Form: Fields for generating compliance reports.";
    }
}

class RegulatorNotificationPanel implements NotificationPanel {
    @Override
    public String showNotifications() {
        return "Showing Regulator Notifications: System alerts and compliance issues.";
    }
}

// Concrete Factories
class PatientViewFactory implements ViewFactory {
    @Override
    public Dashboard createDashboard() {
        return new PatientDashboard();
    }

    @Override
    public Form createForm() {
        return new PatientForm();
    }

    @Override
    public NotificationPanel createNotificationPanel() {
        return new PatientNotificationPanel();
    }
}

class ProviderViewFactory implements ViewFactory {
    @Override
    public Dashboard createDashboard() {
        return new ProviderDashboard();
    }

    @Override
    public Form createForm() {
        return new ProviderForm();
    }

    @Override
    public NotificationPanel createNotificationPanel() {
        return new ProviderNotificationPanel();
    }
}

class RegulatorViewFactory implements ViewFactory {
    @Override
    public Dashboard createDashboard() {
        return new RegulatorDashboard();
    }

    @Override
    public Form createForm() {
        return new RegulatorForm();
    }

    @Override
    public NotificationPanel createNotificationPanel() {
        return new RegulatorNotificationPanel();
    }
}

