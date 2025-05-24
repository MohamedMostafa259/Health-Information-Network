package org.example.dto;

import lombok.Data;
import javax.validation.constraints.*;

@Data
public class MedicalRecordDTO {
    private Long id;
    
    @NotNull(message = "Patient ID is required")
    private Long patientId;
    
    @NotBlank(message = "Diagnosis is required")
    private String diagnosis;
    
    @NotBlank(message = "Treatment is required")
    private String treatment;
    
    private String notes;
} 