package com.healthinformationnetwork.patterns.flyweight;

import java.util.HashMap;
import java.util.Map;

public class MedicalCode {
    private static final Map<String, MedicalCode> codeCache = new HashMap<>();
    private final String code;
    private final String description;

    private MedicalCode(String code, String description) {
        this.code = code;
        this.description = description;
    }

    public static MedicalCode getCode(String code, String description) {
        return codeCache.computeIfAbsent(code, k -> new MedicalCode(code, description));
    }

    public String getCode() {
        return code;
    }

    public String getDescription() {
        return description;
    }
} 