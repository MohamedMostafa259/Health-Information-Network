package model;

public class Patient {
    private int patientID;
    private String name;
    private String phoneNo;
    private String nationalID;
    private boolean insuranceStatus;
    private String birthdate;
    private String gender;
    private String email;
    private int age;
    private int insuranceID;
    private int packageID;

    // Getters and Setters
    public int getPatientID() { return patientID; }
    public void setPatientID(int patientID) { this.patientID = patientID; }
    public String getName() { return name; }
    public void setName(String name) { this.name = name; }
    public String getPhoneNo() { return phoneNo; }
    public void setPhoneNo(String phoneNo) { this.phoneNo = phoneNo; }
    public String getNationalID() { return nationalID; }
    public void setNationalID(String nationalID) { this.nationalID = nationalID; }
    public boolean isInsuranceStatus() { return insuranceStatus; }
    public void setInsuranceStatus(boolean insuranceStatus) { this.insuranceStatus = insuranceStatus; }
    public String getBirthdate() { return birthdate; }
    public void setBirthdate(String birthdate) { this.birthdate = birthdate; }
    public String getGender() { return gender; }
    public void setGender(String gender) { this.gender = gender; }
    public String getEmail() { return email; }
    public void setEmail(String email) { this.email = email; }
    public int getAge() { return age; }
    public void setAge(int age) { this.age = age; }
    public int getInsuranceID() { return insuranceID; }
    public void setInsuranceID(int insuranceID) { this.insuranceID = insuranceID; }
    public int getPackageID() { return packageID; }
    public void setPackageID(int packageID) { this.packageID = packageID; }
}