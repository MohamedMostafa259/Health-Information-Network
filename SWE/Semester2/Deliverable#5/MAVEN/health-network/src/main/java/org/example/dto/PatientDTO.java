package org.example.dto;

import lombok.Data;
import org.example.model.Patient.Gender;
import javax.validation.constraints.*;

@Data
public class PatientDTO {
    private Long id;
    
    @NotBlank(message = "Name is required")
    private String name;
    
    @NotNull(message = "Age is required")
    @Min(value = 0, message = "Age must be positive")
    @Max(value = 150, message = "Age must be less than 150")
    private Integer age;
    
    @NotNull(message = "Gender is required")
    private Gender gender;
    
    @NotBlank(message = "Contact information is required")
    private String contactInfo;
} 