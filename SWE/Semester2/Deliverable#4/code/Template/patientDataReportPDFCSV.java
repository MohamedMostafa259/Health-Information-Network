package SWE.Semester2.Deliverable#4.code.Template;

abstract class PatientReport {
    public final void generateReport() {
        fetchData();
        formatData();
        export();
    }

    protected abstract void fetchData();
    protected abstract void formatData();
    protected abstract void export();
}

class PDFReport extends PatientReport {
    protected void fetchData() {
        System.out.println("Fetching data for PDF report.");
    }
    protected void formatData() {
        System.out.println("Formatting data as PDF.");
    }
    protected void export() {
        System.out.println("Exporting PDF report.");
    }
}

class CSVReport extends PatientReport {
    protected void fetchData() {
        System.out.println("Fetching data for CSV report.");
    }
    protected void formatData() {
        System.out.println("Formatting data as CSV.");
    }
    protected void export() {
        System.out.println("Exporting CSV report.");
    }
}

