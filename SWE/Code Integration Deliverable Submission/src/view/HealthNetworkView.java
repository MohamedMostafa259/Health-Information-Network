package view;

import controller.HealthNetworkController;
import model.Patient;

import javax.swing.*;
import java.awt.*;
import java.util.List;

public class HealthNetworkView extends JFrame {
    private HealthNetworkController controller;

    public HealthNetworkView() {
        controller = new HealthNetworkController();
        setTitle("Health Information Network Management System");
        setSize(800, 600);
        setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        setLayout(new BorderLayout());

        JTable table = new JTable();
        add(new JScrollPane(table), BorderLayout.CENTER);

        JButton loadButton = new JButton("Load Patients");
        loadButton.addActionListener(e -> {
            List<Patient> patients = controller.getAllPatients();
            if (patients.isEmpty()) {
                JOptionPane.showMessageDialog(this, "No patients found or unable to connect to the database.", "Error", JOptionPane.ERROR_MESSAGE);
                return;
            }
            String[] columnNames = {"PatientID", "Name", "PhoneNo", "NationalID", "InsuranceStatus", "Birthdate", "Gender", "Email", "Age", "InsuranceID", "PackageID"};
            String[][] data = new String[patients.size()][columnNames.length];
            for (int i = 0; i < patients.size(); i++) {
                Patient p = patients.get(i);
                data[i][0] = String.valueOf(p.getPatientID());
                data[i][1] = p.getName();
                data[i][2] = p.getPhoneNo();
                data[i][3] = p.getNationalID();
                data[i][4] = String.valueOf(p.isInsuranceStatus());
                data[i][5] = p.getBirthdate();
                data[i][6] = p.getGender();
                data[i][7] = p.getEmail();
                data[i][8] = String.valueOf(p.getAge());
                data[i][9] = String.valueOf(p.getInsuranceID());
                data[i][10] = String.valueOf(p.getPackageID());
            }
            table.setModel(new javax.swing.table.DefaultTableModel(data, columnNames));
        });
        add(loadButton, BorderLayout.SOUTH);
    }

    public static void main(String[] args) {
        SwingUtilities.invokeLater(() -> {
            HealthNetworkView view = new HealthNetworkView();
            view.setVisible(true);
        });
    }
}

// Steps to run the code:
// 1. open the 'tasks.json' file in root directory and build your project "Ctrl + Shift + B"
// 2. write this command in the terminal: java -cp "bin;lib/sqljdbc4.jar" view.HealthNetworkView
