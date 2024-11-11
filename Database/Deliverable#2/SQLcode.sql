-- CREATE DATABASE HIN; -- HIN stands for Health Information Network

CREATE TABLE HealthProvider (
	ProviderID VARCHAR(20) PRIMARY KEY,
	Availability CHAR(20) NOT NULL, -- Format: From 00 am/pm To 00 am/pm
	Specialty VARCHAR(20) NOT NULL,
	Name VARCHAR(50) NOT NULL
);

CREATE TABLE GovernmentRegulator (
	RegulatorID VARCHAR(20) PRIMARY KEY,
	Name VARCHAR(50) NOT NULL, 
	Position VARCHAR(30) NOT NULL
);

CREATE TABLE InsuranceCompany (
	InsuranceID VARCHAR(20) PRIMARY KEY,
	CompanyName VARCHAR(30) NOT NULL,
	Email VARCHAR(30) NOT NULL,
	Phone VARCHAR(11) NOT NULL
);

CREATE TABLE Package (
	PackageID VARCHAR(2) PRIMARY KEY -- we can store up to 100 packages
); 

CREATE TABLE PackageDetails (
	IllnessType VARCHAR(20) NOT NULL,
	Percentage NUMERIC (2, 2) NOT NULL,
	PackageID VARCHAR(2) NOT NULL, 
	PRIMARY KEY (IllnessType, Percentage, PackageID),
	FOREIGN KEY (PackageID) REFERENCES Package(PackageID)
);

CREATE TABLE InsuranceCompanyPackages (
    InsuranceID VARCHAR(20) NOT NULL,
    PackageID VARCHAR(2) NOT NULL,
	PRIMARY KEY (InsuranceID, PackageID),
	FOREIGN KEY (InsuranceID) REFERENCES InsuranceCompany(InsuranceID),
	FOREIGN KEY (PackageID) REFERENCES Package(PackageID)
);

CREATE TABLE Report (
	ReportID VARCHAR(20) PRIMARY KEY,
	ReportType VARCHAR(10) CHECK (ReportType IN ('Medical', 'Analysis')) NOT NULL, 
	GenerateDate DATE NOT NULL
);

CREATE TABLE GovernmentRegulatorReports
(
    ReportID VARCHAR(20) NOT NULL,
    RegulatorID VARCHAR(20) NOT NULL,
    PRIMARY KEY (ReportID, RegulatorID),
	FOREIGN KEY (ReportID) REFERENCES Report(ReportID),
	FOREIGN KEY (RegulatorID) REFERENCES GovernmentRegulator(RegulatorID)
);

CREATE TABLE Patient
(	
	PatientID VARCHAR(20) PRIMARY KEY,
	Name VARCHAR(50) NOT NULL,
	PhoneNo CHAR(11) NOT NULL,
	NationalID CHAR(14) UNIQUE NOT NULL,
	InsuranceStatus BIT NOT NULL, -- similar to BOOLEAN : 0 means not-insured , 1 means insured
	Birthdate DATE NOT NULL,
	Gender VARCHAR(10) CHECK (Gender IN ('Male', 'Female')) NOT NULL,
	Email VARCHAR(30) NOT NULL,
	Age TINYINT NOT NULL, -- TYNYINT is just one byte (from 0 to 255)
	InsuranceID VARCHAR(20) NOT NULL,
    PackageID VARCHAR(2) NOT NULL,
	FOREIGN KEY (InsuranceID) REFERENCES InsuranceCompany(InsuranceID),
	FOREIGN KEY (PackageID) REFERENCES Package(PackageID)
);

CREATE TABLE Appointment
(
	AppointmentID VARCHAR(20) PRIMARY KEY,
	EmergencyStatus VARCHAR(4) CHECK (EmergencyStatus IN ('High', 'Mid', 'Low')) NOT NULL,
    Time DATE NOT NULL,
    Type_of_illness VARCHAR(20) NOT NULL,
    PaymentAmount INT NOT NULL,
    PaymentMethod VARCHAR(6) CHECK (PaymentMethod IN ('Cash', 'Credit', 'Debit')) NOT NULL,
	PatientID VARCHAR(20) NOT NULL,
    FOREIGN KEY (PatientID) REFERENCES Patient(PatientID)
);

CREATE TABLE HealthPoviderAppointments
(
	AppointmentID VARCHAR(20) NOT NULL,
	ProviderID VARCHAR(20) NOT NULL,
	PRIMARY KEY (AppointmentID, ProviderID),
    FOREIGN KEY (ProviderID) REFERENCES HealthProvider(ProviderID),
    FOREIGN KEY (AppointmentID) REFERENCES Appointment(AppointmentID)
);

CREATE TABLE HealthRecord
(
	RecordID VARCHAR(20) PRIMARY KEY,
    TypeOfIncident VARCHAR(20) NOT NULL,
    DateOfIncident DATE NOT NULL,
    Details VARCHAR(500) NOT NULL,
	PatientID VARCHAR(20) NOT NULL,
	AppointmentID VARCHAR(20) NOT NULL,
	ProviderID VARCHAR(20) NOT NULL,
    FOREIGN KEY (PatientID) REFERENCES Patient(PatientID),
    FOREIGN KEY (AppointmentID) REFERENCES Appointment(AppointmentID),
    FOREIGN KEY (ProviderID) REFERENCES HealthProvider(ProviderID)
);

CREATE TABLE Regulator_Access_HealthRecord
(
    RegulatorID VARCHAR(20) NOT NULL,
    RecordID VARCHAR(20) NOT NULL,
    PRIMARY KEY (RegulatorID, RecordID),
	FOREIGN KEY (RegulatorID) REFERENCES GovernmentRegulator(RegulatorID),
    FOREIGN KEY (RecordID) REFERENCES HealthRecord(RecordID)
);

CREATE TABLE Notification
(
	NotificationID VARCHAR(20) PRIMARY KEY,
    Message VARCHAR(500) NOT NULL,
    NotificationType VARCHAR(5) CHECK (NotificationType IN ('Email', 'SMS')) NOT NULL,
    Date DATE NOT NULL,
	PatientID VARCHAR(20) NOT NULL,
	InsuranceID VARCHAR(20) NOT NULL,
	AppointmentID VARCHAR(20) NOT NULL,
    FOREIGN KEY (PatientID) REFERENCES Patient(PatientID),
    FOREIGN KEY (InsuranceID) REFERENCES InsuranceCompany(InsuranceID),
    FOREIGN KEY (AppointmentID) REFERENCES Appointment(AppointmentID)
);

CREATE TABLE ReportGeneration
(
    NotificationID VARCHAR(20) NOT NULL,
    ProviderID VARCHAR(20) NOT NULL,
    ReportID VARCHAR(20) NOT NULL,
	PRIMARY KEY (NotificationID, ProviderID, ReportID),
    FOREIGN KEY (NotificationID) REFERENCES Notification(NotificationID),
    FOREIGN KEY (ProviderID) REFERENCES HealthProvider(ProviderID),
    FOREIGN KEY (ReportID) REFERENCES Report(ReportID)
);

CREATE TABLE Card
(
    CardNumber CHAR(16) PRIMARY KEY,
    ExpirationDate DATE NOT NULL,
    CardHolderName VARCHAR(50) NOT NULL,
    CardType VARCHAR(6) CHECK (CardType IN ('Debit', 'Credit')) NOT NULL,
    BankName VARCHAR(30) NOT NULL,
	PatientID VARCHAR(20) NOT NULL,
    FOREIGN KEY (PatientID) REFERENCES Patient(PatientID)
);

CREATE TABLE Caregiver
(
    Relationship VARCHAR(15) NOT NULL,
    Name VARCHAR(50) NOT NULL,
    Phone CHAR(11) NOT NULL,
    Email VARCHAR(30) NOT NULL,
    PRIMARY KEY (Relationship, Name)
);

CREATE TABLE CaregiversOfPatients
(
    PatientID VARCHAR(20) NOT NULL,
    Relationship VARCHAR(15) NOT NULL,
    Name VARCHAR(50) NOT NULL,
	PRIMARY KEY (PatientID, Name, Relationship),
    FOREIGN KEY (PatientID) REFERENCES Patient(PatientID),
    FOREIGN KEY (Relationship, Name) REFERENCES Caregiver(Relationship, Name)
);

CREATE TABLE CaregiversNotifications
(
    Relationship VARCHAR(15) NOT NULL,
    Name VARCHAR(50) NOT NULL,
    NotificationID VARCHAR(20) NOT NULL,
	PatientID VARCHAR(20) NOT NULL,
	PRIMARY KEY (PatientID, Name, NotificationID),
    FOREIGN KEY (Relationship, Name) REFERENCES Caregiver(Relationship, Name),
    FOREIGN KEY (NotificationID) REFERENCES Notification(NotificationID)
);


/***************  Populating The Database ***************/

-- Fix for Patient table: Cannot have NULL InsuranceID/PackageID
ALTER TABLE Patient
ALTER COLUMN InsuranceID VARCHAR(20) NULL;
ALTER TABLE Patient
ALTER COLUMN PackageID VARCHAR(2) NULL;

-- Now populate tables in correct order to respect foreign key constraints
-- First, populate base tables that don't depend on others

-- HealthProvider (no changes needed)
INSERT INTO HealthProvider (ProviderID, Availability, Specialty, Name) VALUES
('HP001', '09 am To 05 pm', 'Cardiology', 'Dr. Sarah Johnson'),
('HP002', '10 am To 06 pm', 'Pediatrics', 'Dr. Michael Chen'),
('HP003', '08 am To 04 pm', 'Orthopedics', 'Dr. James Wilson'),
('HP004', '11 am To 07 pm', 'Dermatology', 'Dr. Emily Rodriguez'),
('HP005', '09 am To 05 pm', 'Neurology', 'Dr. David Kim');

-- GovernmentRegulator (no changes needed)
INSERT INTO GovernmentRegulator (RegulatorID, Name, Position) VALUES
('REG001', 'John Smith', 'Chief Medical Officer'),
('REG002', 'Lisa Anderson', 'Health Inspector'),
('REG003', 'Robert Brown', 'Policy Director'),
('REG004', 'Maria Garcia', 'Compliance Officer'),
('REG005', 'William Lee', 'Quality Assessor');

-- InsuranceCompany (no changes needed)
INSERT INTO InsuranceCompany (InsuranceID, CompanyName, Email, Phone) VALUES
('INS001', 'HealthGuard', 'info@healthguard.com', '18005551234'),
('INS002', 'MediCare Plus', 'contact@medicare.com', '18005555678'),
('INS003', 'WellCare', 'support@wellcare.com', '18005559012'),
('INS004', 'Shield Insurance', 'help@shield.com', '18005553456'),
('INS005', 'Care First', 'info@carefirst.com', '18005557890');

-- Package (no changes needed)
INSERT INTO Package (PackageID) VALUES
('P1'), ('P2'), ('P3'), ('P4'), ('P5');

-- PackageDetails (no changes needed)
INSERT INTO PackageDetails (IllnessType, Percentage, PackageID) VALUES
('Chronic', 0.80, 'P1'),
('Emergency', 0.90, 'P1'),
('Routine', 0.70, 'P2'),
('Preventive', 0.85, 'P3'),
('Surgical', 0.95, 'P4'),
('Dental', 0.60, 'P5');

-- InsuranceCompanyPackages (no changes needed)
INSERT INTO InsuranceCompanyPackages (InsuranceID, PackageID) VALUES
('INS001', 'P1'),
('INS001', 'P2'),
('INS002', 'P3'),
('INS003', 'P4'),
('INS004', 'P5'),
('INS005', 'P1');

-- Patient (modified to handle NULL insurance for uninsured patients)
INSERT INTO Patient (PatientID, Name, PhoneNo, NationalID, InsuranceStatus, Birthdate, Gender, Email, Age, InsuranceID, PackageID) VALUES
('PAT001', 'Alice Thompson', '12345678901', '12345678901234', 1, '1990-05-15', 'Female', 'alice@email.com', 33, 'INS001', 'P1'),
('PAT002', 'Bob Martinez', '23456789012', '23456789012345', 1, '1985-08-22', 'Male', 'bob@email.com', 38, 'INS002', 'P3'),
('PAT003', 'Carol White', '34567890123', '34567890123456', 0, '1995-03-10', 'Female', 'carol@email.com', 28, NULL, NULL),
('PAT004', 'Daniel Lee', '45678901234', '45678901234567', 1, '1978-11-30', 'Male', 'daniel@email.com', 45, 'INS003', 'P4'),
('PAT005', 'Emma Davis', '56789012345', '56789012345678', 1, '1992-07-25', 'Female', 'emma@email.com', 31, 'INS001', 'P2');

-- Appointment
INSERT INTO Appointment (AppointmentID, EmergencyStatus, Time, Type_of_illness, PaymentAmount, PaymentMethod, PatientID) VALUES
('APT001', 'Low', '2024-01-20', 'Routine Checkup', 150, 'Cash', 'PAT001'),
('APT002', 'High', '2024-02-05', 'Chest Pain', 500, 'Credit', 'PAT002'),
('APT003', 'Mid', '2024-02-10', 'Sprain', 250, 'Debit', 'PAT003'),
('APT004', 'Low', '2024-03-01', 'Vaccination', 100, 'Cash', 'PAT004'),
('APT005', 'High', '2024-03-10', 'Migraine', 300, 'Credit', 'PAT005');

-- Report
INSERT INTO Report (ReportID, ReportType, GenerateDate) VALUES
('REP001', 'Medical', '2024-01-15'),
('REP002', 'Medical', '2024-02-01'),
('REP003', 'Analysis', '2024-02-15'),
('REP004', 'Analysis', '2024-03-01'),
('REP005', 'Medical', '2024-03-15');

-- HealthProviderAppointments
INSERT INTO HealthPoviderAppointments (AppointmentID, ProviderID) VALUES
('APT001', 'HP001'),
('APT002', 'HP001'),
('APT003', 'HP003'),
('APT004', 'HP002'),
('APT005', 'HP005');

-- HealthRecord
INSERT INTO HealthRecord (RecordID, TypeOfIncident, DateOfIncident, Details, PatientID, AppointmentID, ProviderID) VALUES
('REC001', 'Routine Checkup', '2024-01-20', 'Annual physical examination - all vitals normal', 'PAT001', 'APT001', 'HP001'),
('REC002', 'Emergency', '2024-02-05', 'Acute chest pain - EKG performed', 'PAT002', 'APT002', 'HP001'),
('REC003', 'Injury', '2024-02-10', 'Ankle sprain - prescribed rest and compression', 'PAT003', 'APT003', 'HP003'),
('REC004', 'Preventive', '2024-03-01', 'Seasonal flu vaccination administered', 'PAT004', 'APT004', 'HP002'),
('REC005', 'Emergency', '2024-03-10', 'Severe migraine - prescribed medication', 'PAT005', 'APT005', 'HP005');

-- Regulator_Access_HealthRecord
INSERT INTO Regulator_Access_HealthRecord (RegulatorID, RecordID) VALUES
('REG001', 'REC001'),
('REG002', 'REC002'),
('REG003', 'REC003');

-- GovernmentRegulatorReports
INSERT INTO GovernmentRegulatorReports (ReportID, RegulatorID) VALUES
('REP003', 'REG001'),
('REP004', 'REG002');

-- First, modify the Notification table to allow NULL InsuranceID
ALTER TABLE Notification
ALTER COLUMN InsuranceID VARCHAR(20) NULL;

-- Now insert data in the correct order to maintain referential integrity

-- Notification table needs to be populated before ReportGeneration and CaregiversNotifications
INSERT INTO Notification (NotificationID, Message, NotificationType, Date, PatientID, InsuranceID, AppointmentID) VALUES
('NOT001', 'Appointment reminder for checkup', 'Email', '2024-01-19', 'PAT001', 'INS001', 'APT001'),
('NOT002', 'Emergency appointment confirmed', 'SMS', '2024-02-05', 'PAT002', 'INS002', 'APT002'),
('NOT003', 'Follow-up appointment needed', 'Email', '2024-02-11', 'PAT003', NULL, 'APT003'),
('NOT004', 'Vaccination due reminder', 'SMS', '2024-02-28', 'PAT004', 'INS003', 'APT004'),
('NOT005', 'Prescription ready for pickup', 'Email', '2024-03-10', 'PAT005', 'INS001', 'APT005');


-- ReportGeneration
INSERT INTO ReportGeneration (NotificationID, ProviderID, ReportID) VALUES
('NOT001', 'HP001', 'REP001'),
('NOT002', 'HP001', 'REP002'),
('NOT005', 'HP005', 'REP005');

-- Card
INSERT INTO Card (CardNumber, ExpirationDate, CardHolderName, CardType, BankName, PatientID) VALUES
('4532789012345678', '2025-12-31', 'Alice Thompson', 'Credit', 'CitiBank', 'PAT001'),
('5678901234567890', '2026-06-30', 'Bob Martinez', 'Debit', 'Chase', 'PAT002'),
('4111567890123456', '2025-09-30', 'Daniel Lee', 'Credit', 'Wells Fargo', 'PAT004'),
('5432109876543210', '2026-03-31', 'Emma Davis', 'Debit', 'Bank of America', 'PAT005');

-- Caregiver
INSERT INTO Caregiver (Relationship, Name, Phone, Email) VALUES
('Spouse', 'John Thompson', '98765432101', 'john.t@email.com'),
('Parent', 'Maria Martinez', '87654321012', 'maria.m@email.com'),
('Sibling', 'Sarah White', '76543210123', 'sarah.w@email.com'),
('Child', 'Sophie Lee', '65432101234', 'sophie.l@email.com'),
('Spouse', 'Mark Davis', '54321012345', 'mark.d@email.com');

-- CaregiversOfPatients
INSERT INTO CaregiversOfPatients (PatientID, Relationship, Name) VALUES
('PAT001', 'Spouse', 'John Thompson'),
('PAT002', 'Parent', 'Maria Martinez'),
('PAT003', 'Sibling', 'Sarah White'),
('PAT004', 'Child', 'Sophie Lee'),
('PAT005', 'Spouse', 'Mark Davis');

-- CaregiversNotifications (fixed to include PatientID)
INSERT INTO CaregiversNotifications (Relationship, Name, NotificationID, PatientID) VALUES
('Spouse', 'John Thompson', 'NOT001', 'PAT001'),
('Parent', 'Maria Martinez', 'NOT002', 'PAT002'),
('Sibling', 'Sarah White', 'NOT003', 'PAT003'),
('Child', 'Sophie Lee', 'NOT004', 'PAT004'),
('Spouse', 'Mark Davis', 'NOT005', 'PAT005');