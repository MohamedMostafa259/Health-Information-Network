/* IDEA:
In a health information system, users (patients, doctors, admins) 
may need to export medical records or reports in different formats (PDF, CSV, XML, JSON, etc.).
Using the Strategy Pattern, you can allow the system to choose the export format at runtime, 
making it easy to add new formats in the future.
*/

// Strategy Interface
interface DataExportStrategy {
    void export(String data, String fileName);
}

// Concrete Strategy: PDF Export
class PDFExportStrategy implements DataExportStrategy {
    public void export(String data, String fileName) {
        System.out.println("Exporting data to PDF file: " + fileName + ".pdf");
    }
}

// Concrete Strategy: CSV Export
class CSVExportStrategy implements DataExportStrategy {
    public void export(String data, String fileName) {
        System.out.println("Exporting data to CSV file: " + fileName + ".csv");
    }
}

// Concrete Strategy: JSON Export
class JSONExportStrategy implements DataExportStrategy {
    public void export(String data, String fileName) {
        System.out.println("Exporting data to JSON file: " + fileName + ".json");
    }
}

// Context
class DataExporter {
    private DataExportStrategy strategy;
    public void setStrategy(DataExportStrategy strategy) {
        this.strategy = strategy;
    }
    public void exportData(String data, String fileName) {
        strategy.export(data, fileName);
    }
}

// Client 
public class Client {
    public static void main(String[] args) {
        DataExporter exporter = new DataExporter();
        String sampleData = "Patient Name, Date, Diagnosis\nJohn Doe, 2024-06-01, Healthy";

        exporter.setStrategy(new PDFExportStrategy());
        exporter.exportData(sampleData, "PDFreport");

        exporter.setStrategy(new CSVExportStrategy());
        exporter.exportData(sampleData, "CSVreport");

        exporter.setStrategy(new JSONExportStrategy());
        exporter.exportData(sampleData, "JSONreport");
    }
}

