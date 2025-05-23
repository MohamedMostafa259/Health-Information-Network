@RestController
@RequestMapping("/patients")
public class PatientController {

    @Autowired
    private PatientService patientService;

    @GetMapping("/{patientId}/records")
    public ResponseEntity<PatientRecordDTO> getPatientRecords(@PathVariable String patientId) {
        PatientRecordDTO record = patientService.getPatientRecords(patientId);
        return ResponseEntity.ok(record);
    }
}
