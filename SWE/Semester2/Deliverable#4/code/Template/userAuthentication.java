package SWE.Semester2.Deliverable#4.code.Template;

abstract class Authenticator {
    public final void authenticate() {
        validateCredentials();
        logAccess();
        postLogin();
    }

    protected abstract void validateCredentials();
    protected void logAccess() {
        System.out.println("Logging access.");
    }
    protected abstract void postLogin();
}

class DoctorAuthenticator extends Authenticator {
    protected void validateCredentials() {
        System.out.println("Validating doctor credentials.");
    }
    protected void postLogin() {
        System.out.println("Doctor dashboard loaded.");
    }
}

class PatientAuthenticator extends Authenticator {
    protected void validateCredentials() {
        System.out.println("Validating patient credentials.");
    }
    protected void postLogin() {
        System.out.println("Patient dashboard loaded.");
    }
}
