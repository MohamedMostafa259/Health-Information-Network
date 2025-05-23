@Data
public class PatientRecordDTO {
    private String patientId;
    private String name;
    private LocalDate dateOfBirth;
    private List<Visit> visits = new ArrayList<>();
    private List<LabResult> labResults = new ArrayList<>();

    @Data
    public static class Visit {
        private LocalDate date;
        private String diagnosis;
        private List<String> prescription;
    }

    @Data
    public static class LabResult {
        private LocalDate date;
        private String type;
        private String result;
    }
}
