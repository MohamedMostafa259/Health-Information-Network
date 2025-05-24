package org.example.controller;

import org.example.dto.MedicalRecordDTO;
import org.example.model.MedicalRecord;
import org.example.model.Patient;
import org.example.repository.MedicalRecordRepository;
import org.example.repository.PatientRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.validation.annotation.Validated;
import org.springframework.web.bind.annotation.*;

import javax.validation.Valid;

@RestController
@RequestMapping("/api/medical-records")
@Validated
public class MedicalRecordController {

    @Autowired
    private MedicalRecordRepository medicalRecordRepository;

    @Autowired
    private PatientRepository patientRepository;

    // POST new medical record
    @PostMapping
    public ResponseEntity<MedicalRecordDTO> createMedicalRecord(@Valid @RequestBody MedicalRecordDTO medicalRecordDTO) {
        try {
            return patientRepository.findById(medicalRecordDTO.getPatientId())
                    .map(patient -> {
                        MedicalRecord medicalRecord = convertToEntity(medicalRecordDTO, patient);
                        MedicalRecord savedRecord = medicalRecordRepository.save(medicalRecord);
                        return ResponseEntity.status(HttpStatus.CREATED).body(convertToDTO(savedRecord));
                    })
                    .orElse(ResponseEntity.status(HttpStatus.NOT_FOUND).build());
        } catch (Exception e) {
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).build();
        }
    }

    private MedicalRecordDTO convertToDTO(MedicalRecord record) {
        MedicalRecordDTO dto = new MedicalRecordDTO();
        dto.setId(record.getId());
        dto.setPatientId(record.getPatient().getId());
        dto.setDiagnosis(record.getDiagnosis());
        dto.setTreatment(record.getTreatment());
        dto.setNotes(record.getNotes());
        return dto;
    }

    private MedicalRecord convertToEntity(MedicalRecordDTO dto, Patient patient) {
        MedicalRecord record = new MedicalRecord();
        record.setPatient(patient);
        record.setDiagnosis(dto.getDiagnosis());
        record.setTreatment(dto.getTreatment());
        record.setNotes(dto.getNotes());
        return record;
    }
} 