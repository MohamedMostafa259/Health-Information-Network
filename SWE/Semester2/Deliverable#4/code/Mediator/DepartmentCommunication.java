package SWE.Semester2.Deliverable#4.code.Mediator;

interface Department {
    void send(String message, String to);
    void receive(String message);
}

class HospitalMediator {
    Lab lab;
    Pharmacy pharmacy;
    Radiology radiology;

    void sendMessage(String message, String to) {
        switch (to) {
            case "Lab" -> lab.receive(message);
            case "Pharmacy" -> pharmacy.receive(message);
            case "Radiology" -> radiology.receive(message);
        }
    }
}

class Lab implements Department {
    HospitalMediator mediator;
    Lab(HospitalMediator m) { this.mediator = m; m.lab = this; }

    public void send(String message, String to) {
        mediator.sendMessage(message, to);
    }
    public void receive(String message) {
        System.out.println("Lab received: " + message);
    }
}

class Pharmacy implements Department {
    HospitalMediator mediator;
    Pharmacy(HospitalMediator m) { this.mediator = m; m.pharmacy = this; }

    public void send(String message, String to) {
        mediator.sendMessage(message, to);
    }
    public void receive(String message) {
        System.out.println("Pharmacy received: " + message);
    }
}

class Radiology implements Department {
    HospitalMediator mediator;
    Radiology(HospitalMediator m) { this.mediator = m; m.radiology = this; }

    public void send(String message, String to) {
        mediator.sendMessage(message, to);
    }
    public void receive(String message) {
        System.out.println("Radiology received: " + message);
    }
}
