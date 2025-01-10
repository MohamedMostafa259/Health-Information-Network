package view;

import controller.HealthNetworkController;
import model.Patient;
import model.DatabaseConnection;  

import javax.swing.*;
import javax.swing.table.DefaultTableModel;

import java.awt.*;
import java.util.List;

public class HealthNetworkView extends JFrame {
    private HealthNetworkController controller;
    private JTable table;
    private JButton loadButton;
    private JButton addButton;

    public HealthNetworkView() {
        controller = new HealthNetworkController();
        initializeUI();

        // Add shutdown hook to close database connection
        Runtime.getRuntime().addShutdownHook(new Thread(() -> {
            DatabaseConnection.closeConnection();
        }));
        
        // Also add window listener to handle closing
        addWindowListener(new java.awt.event.WindowAdapter() {
            @Override
            public void windowClosing(java.awt.event.WindowEvent windowEvent) {
                DatabaseConnection.closeConnection();
            }
        });
    }

    private void initializeUI() {
        setTitle("Health Information Network Management System");
        setSize(800, 600);
        setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        setLayout(new BorderLayout());

        // Create table
        table = new JTable();
        add(new JScrollPane(table), BorderLayout.CENTER);

        // Create button panel
        JPanel buttonPanel = new JPanel();
        loadButton = new JButton("Load Patients");
        addButton = new JButton("Add Patient");
        
        loadButton.addActionListener(e -> loadPatients());
        addButton.addActionListener(e -> showAddPatientDialog());
        
        buttonPanel.add(loadButton);
        buttonPanel.add(addButton);
        add(buttonPanel, BorderLayout.SOUTH);
    }

    private void loadPatients() {
        // clear the existing table model first
        table.setModel(new DefaultTableModel());
        
        List<Patient> patients = controller.getAllPatients();
        if (patients.isEmpty()) {
            JOptionPane.showMessageDialog(this, 
                "No patients found in the database.", 
                "Information", 
                JOptionPane.INFORMATION_MESSAGE);
            return;
        }

        String[] columnNames = {
            "Patient ID", "Name", "Phone", "National ID", "Insurance", 
            "Birthdate", "Gender", "Email", "Age", "Insurance ID", "Package ID"
        };
        
        Object[][] data = new Object[patients.size()][columnNames.length];
        for (int i = 0; i < patients.size(); i++) {
            Patient p = patients.get(i);
            data[i] = new Object[]{
                p.getPatientID(), p.getName(), p.getPhoneNo(), 
                p.getNationalID(), p.isInsuranceStatus(), p.getBirthdate(),
                p.getGender(), p.getEmail(), p.getAge(), 
                p.getInsuranceID(), p.getPackageID()
            };
        }
        
        table.setModel(new DefaultTableModel(data, columnNames));
    }

    private void showAddPatientDialog() {
        // Create a form for adding a new patient
        JDialog dialog = new JDialog(this, "Add New Patient", true);
        dialog.setLayout(new GridLayout(0, 2, 5, 5));

        // Add form fields
        JTextField patientIDField = new JTextField();
        JTextField nameField = new JTextField();
        JTextField phoneField = new JTextField();
        JTextField nationalIDField = new JTextField();
        JCheckBox insuranceBox = new JCheckBox();
        JTextField birthdateField = new JTextField();
        JTextField genderField = new JTextField();
        JTextField emailField = new JTextField();
        JTextField ageField = new JTextField();
        JTextField insuranceIDField = new JTextField();
        JTextField packageIDField = new JTextField();

        dialog.add(new JLabel("Patient ID:"));
        dialog.add(patientIDField);
        dialog.add(new JLabel("Name:"));
        dialog.add(nameField);
        dialog.add(new JLabel("Phone:"));
        dialog.add(phoneField);
        dialog.add(new JLabel("National ID:"));
        dialog.add(nationalIDField);
        dialog.add(new JLabel("Insurance Status:"));
        dialog.add(insuranceBox);
        dialog.add(new JLabel("Birthdate:"));
        dialog.add(birthdateField);
        dialog.add(new JLabel("Gender:"));
        dialog.add(genderField);
        dialog.add(new JLabel("Email:"));
        dialog.add(emailField);
        dialog.add(new JLabel("Age:"));
        dialog.add(ageField);
        dialog.add(new JLabel("Insurance ID:"));
        dialog.add(insuranceIDField);
        dialog.add(new JLabel("Package ID:"));
        dialog.add(packageIDField);

        JButton saveButton = new JButton("Save");
        saveButton.addActionListener(e -> {
            try {
                Patient patient = new Patient();
                patient.setPatientID(patientIDField.getText());
                patient.setName(nameField.getText());
                patient.setPhoneNo(phoneField.getText());
                patient.setNationalID(nationalIDField.getText());
                patient.setInsuranceStatus(insuranceBox.isSelected());
                patient.setBirthdate(birthdateField.getText());
                patient.setGender(genderField.getText());
                patient.setEmail(emailField.getText());
                patient.setAge(Integer.parseInt(ageField.getText()));
                patient.setInsuranceID(insuranceIDField.getText());
                patient.setPackageID(packageIDField.getText());

                if (controller.addPatient(patient)) {
                    JOptionPane.showMessageDialog(dialog, 
                        "Patient added successfully!", 
                        "Success", 
                        JOptionPane.INFORMATION_MESSAGE);
                    dialog.dispose();
                    loadPatients(); // Refresh the table
                } else {
                    JOptionPane.showMessageDialog(dialog, 
                        "Failed to add patient.", 
                        "Error", 
                        JOptionPane.ERROR_MESSAGE);
                }
            } catch (NumberFormatException ex) {
                JOptionPane.showMessageDialog(dialog, 
                    "Please enter valid numbers for Age, Insurance ID, and Package ID", 
                    "Input Error", 
                    JOptionPane.ERROR_MESSAGE);
            }
        });

        dialog.add(saveButton);
        dialog.pack();
        dialog.setLocationRelativeTo(this);
        dialog.setVisible(true);
    }

    public static void main(String[] args) {
        SwingUtilities.invokeLater(() -> {
            HealthNetworkView view = new HealthNetworkView();
            view.setVisible(true);
        });
    }
}

