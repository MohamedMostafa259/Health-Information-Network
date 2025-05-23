@Service
public class PatientService {

    public PatientRecordDTO getPatientRecords(String patientId) {
        // Stubbed mock data
        PatientRecordDTO dto = new PatientRecordDTO();
        dto.setPatientId(patientId);
        dto.setName("Ahmed Ibrahim");
        dto.setDateOfBirth(LocalDate.of(1990, 1, 1));

        // You can populate visit/lab result lists as needed
        return dto;
    }
}
