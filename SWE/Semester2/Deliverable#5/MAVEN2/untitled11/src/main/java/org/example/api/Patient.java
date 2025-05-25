package org.example.api;

public class Patient {
    public int id;
    public String name;
    public String illness;

    public Patient() {}

    public Patient(int id, String name, String illness) {
        this.id = id;
        this.name = name;
        this.illness = illness;
    }
}
