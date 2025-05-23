@Service
public class AppointmentService {

    public List<AppointmentDTO> getAppointments(String doctorId, LocalDate date) {
        // Stubbed mock data
        List<AppointmentDTO> list = new ArrayList<>();
        list.add(new AppointmentDTO("A001", "Fatma El-Sayed", "09:00", "Confirmed"));
        list.add(new AppointmentDTO("A002", "Mohamed Hossam", "10:00", "Pending"));
        return list;
    }
}
