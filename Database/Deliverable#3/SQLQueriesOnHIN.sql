USE [Health Information Network]

/***************************************  MOHAMED MOSTAFA | 22-101203 ***************************************/

-- 1. Get patient appointment history (Patient Name, Appointment Time, Type ofillness) 
--		with provider details (Provider Name, Specialty) and payment info (PaymentAmount, PaymentMethod)
--		Order them decsendingly by appointment time
-- Frequency: Daily - For patient history lookups
SELECT 
    p.Name AS PatientName,
    hp.Name AS ProviderName,
    hp.Specialty,
    a.Time,
    a.Type_of_illness,
    a.PaymentAmount,
    a.PaymentMethod
FROM Patient p
JOIN Appointment a ON p.PatientID = a.PatientID
JOIN HealthPoviderAppointments hpa ON a.AppointmentID = hpa.AppointmentID
JOIN HealthProvider hp ON hpa.ProviderID = hp.ProviderID
WHERE p.PatientID = 'PAT001'
ORDER BY a.Time DESC;

-- 2. Find provider names and specialties with the total number emergency appointments with them
--		Order them decsendingly by 'total number of emergency appointments'
SELECT 
    hp.Name,
    hp.Specialty,
    COUNT(*) AS EmergencyCount
FROM HealthProvider hp
JOIN HealthPoviderAppointments hpa ON hp.ProviderID = hpa.ProviderID
JOIN Appointment a ON hpa.AppointmentID = a.AppointmentID
WHERE a.EmergencyStatus = 'High'
GROUP BY hp.Name, hp.Specialty
ORDER BY EmergencyCount DESC;

-- 3. Calculate insurance coverage statistics by package (CompanyName, PackageID, EnrolledPatients, AverageCoverage)
-- Frequency: Yearly - For insurance analysis
SELECT 
    ic.CompanyName,
    p.PackageID,
    COUNT(pt.PatientID) AS EnrolledPatients,
    AVG(pd.Percentage) AS AverageCoverage
FROM InsuranceCompany ic
JOIN InsuranceCompanyPackages icp ON ic.InsuranceID = icp.InsuranceID
JOIN Package p ON icp.PackageID = p.PackageID
JOIN PackageDetails pd ON p.PackageID = pd.PackageID
LEFT JOIN Patient pt ON ic.InsuranceID = pt.InsuranceID
GROUP BY ic.CompanyName, p.PackageID;

---- 4. Find patients without recent appointments
---- Frequency: Weekly - For follow-up reminders
--SELECT 
--    p.Name,
--    p.Email,
--    p.PhoneNo,
--    MAX(a.Time) AS LastAppointment
--FROM Patient p
--LEFT JOIN Appointment a ON p.PatientID = a.PatientID
--GROUP BY p.Name, p.Email, p.PhoneNo
--HAVING MAX(a.Time) < DATEADD(MONTH, -3, GETDATE())
--    OR MAX(a.Time) IS NULL;

-- 5. Calculate average payment amounts by specialty and emergency status. 
--		Display a column for the number of appointments for each specialty and emergency status as well.
-- Frequency: Monthly - For financial analysis
SELECT 
    hp.Specialty,
    a.EmergencyStatus,
    AVG(a.PaymentAmount) AS AvgPayment,
    COUNT(*) AS AppointmentCount
FROM HealthProvider hp
JOIN HealthPoviderAppointments hpa ON hp.ProviderID = hpa.ProviderID
JOIN Appointment a ON hpa.AppointmentID = a.AppointmentID
GROUP BY hp.Specialty, a.EmergencyStatus;

-- 6. Find patients with multiple caregivers and their notification preferences
-- Frequency: Monthly - For communication management
SELECT 
    p.Name AS PatientName,
    COUNT(DISTINCT c.Name) AS NumCaregivers,
    STRING_AGG(n.NotificationType, ',') AS NotificationTypes
FROM Patient p
JOIN Caregiver c ON p.PatientID = c.PatientID
JOIN CaregiversNotifications cn ON c.PatientID = cn.PatientID
JOIN Notification n ON cn.NotificationID = n.NotificationID
GROUP BY p.Name
HAVING COUNT(DISTINCT c.Name) > 1;

-- 7. Find insurance companies with highest coverage percentages
-- Frequency: Quarterly - For insurance analysis
SELECT 
    ic.CompanyName,
    AVG(pd.Percentage) AS AvgCoverage,
    COUNT(DISTINCT p.PatientID) AS EnrolledPatients
FROM InsuranceCompany ic
JOIN InsuranceCompanyPackages icp ON ic.InsuranceID = icp.InsuranceID
JOIN PackageDetails pd ON icp.PackageID = pd.PackageID
LEFT JOIN Patient p ON ic.InsuranceID = p.InsuranceID
GROUP BY ic.CompanyName
ORDER BY AvgCoverage DESC;

-- 8. Track provider availability and appointment load
-- Frequency: Daily - For scheduling optimization
SELECT 
    hp.Name,
    hp.Availability,
    COUNT(a.AppointmentID) AS DailyAppointments
FROM HealthProvider hp
LEFT JOIN HealthPoviderAppointments hpa ON hp.ProviderID = hpa.ProviderID
LEFT JOIN Appointment a ON hpa.AppointmentID = a.AppointmentID
    AND CONVERT(DATE, a.Time) = CONVERT(DATE, GETDATE())
GROUP BY hp.Name, hp.Availability;

-- 9. Analyze health records by incident type and provider
-- Frequency: Monthly - For quality assessment
SELECT 
    hr.TypeOfIncident,
    hp.Specialty,
    COUNT(*) AS IncidentCount,
    AVG(a.PaymentAmount) AS AvgCost
FROM HealthRecord hr
JOIN HealthProvider hp ON hr.ProviderID = hp.ProviderID
JOIN Appointment a ON hr.AppointmentID = a.AppointmentID
GROUP BY hr.TypeOfIncident, hp.Specialty
ORDER BY IncidentCount DESC;

-- 10. Find patients with expired cards
-- Frequency: Daily - For payment validation
SELECT 
    p.Name AS PatientName,
    c.CardType,
    c.ExpirationDate,
    c.BankName
FROM Patient p
JOIN Card c ON p.PatientID = c.PatientID
WHERE c.ExpirationDate < GETDATE();

---

-- 10. Find providers who generate more notifications than average.
-- Frequency: Useful for tracking communication efficiency.
SELECT ProviderID, Name
FROM HealthProvider
WHERE ProviderID IN (
    SELECT ProviderID
    FROM ReportGeneration
    GROUP BY ProviderID
    HAVING COUNT(NotificationID) > (
        SELECT AVG(notification_count)
        FROM (
            SELECT ProviderID, COUNT(NotificationID) AS notification_count
            FROM ReportGeneration
            GROUP BY ProviderID
        ) AS temp
    )
);

-- 11. List patients receiving notifications more frequently than the average.
-- Frequency: Common in patient engagement metrics.
SELECT PatientID, Name
FROM Patient
WHERE PatientID IN (
    SELECT PatientID
    FROM Notification
    GROUP BY PatientID
    HAVING COUNT(NotificationID) > (
        SELECT AVG(notification_count)
        FROM (
            SELECT PatientID, COUNT(NotificationID) AS notification_count
            FROM Notification
            GROUP BY PatientID
        ) AS temp
    )
);

-- 12. Retrieve appointments scheduled after the last appointment for a specific patient.
-- Frequency: Used in patient appointment tracking.
SELECT AppointmentID, Time
FROM Appointment
WHERE Time > (
    SELECT MAX(Time)
    FROM Appointment
    WHERE PatientID = 'P123'
);



/***************************************  YOUSSEF WALEED  ***************************************/



/***************************************  MOHAMED IBRAHIM   ***************************************/



/***************************************  ADHAM SOBHY  ***************************************/


----











