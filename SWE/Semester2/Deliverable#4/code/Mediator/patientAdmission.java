package SWE.Semester2.Deliverable#4.code.Mediator;

interface Component {
    void execute();
}

class AdmissionMediator {
    Billing billing = new Billing(this);
    DoctorAssignment doctor = new DoctorAssignment(this);
    RoomAllocation room = new RoomAllocation(this);

    void admitPatient() {
        billing.execute();
        doctor.execute();
        room.execute();
    }
}

class Billing implements Component {
    AdmissionMediator mediator;
    Billing(AdmissionMediator m) { this.mediator = m; }

    public void execute() {
        System.out.println("Billing processed.");
    }
}

class DoctorAssignment implements Component {
    AdmissionMediator mediator;
    DoctorAssignment(AdmissionMediator m) { this.mediator = m; }

    public void execute() {
        System.out.println("Doctor assigned.");
    }
}

class RoomAllocation implements Component {
    AdmissionMediator mediator;
    RoomAllocation(AdmissionMediator m) { this.mediator = m; }

    public void execute() {
        System.out.println("Room allocated.");
    }
}
