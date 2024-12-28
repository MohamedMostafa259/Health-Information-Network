import io
import tkinter as tk
from tkinter import ttk, messagebox, filedialog

import numpy as np
import pyodbc
from datetime import datetime
from reportlab.lib.units import inch
from matplotlib import pyplot as plt
from reportlab.lib.pagesizes import letter
from reportlab.lib.utils import ImageReader
from reportlab.pdfgen import canvas


class HealthNetworkApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Health Information Network Management System")
        self.root.geometry("1200x700")
        
        # Database connection
        self.conn = self.connect_to_db()
        
        # Bind the close event
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        # Main frame
        self.main_frame = ttk.Frame(self.root, padding="10")
        self.main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Initialize UI
        self.create_table_selection()
        
    def connect_to_db(self):
        try:
            connection_string = (
                r"Driver={SQL Server};"
                # Change it based on your server name
                r"Server=MOHAMED\MSSQLSERVER01;"  
                r"Database=HIN;"
                r"Trusted_Connection=yes;"
            )
            return pyodbc.connect(connection_string)
        except Exception as e:
            messagebox.showerror("Database Error", f"Error connecting to database: {e}")
            return None

    def close_db_connection(self):
        try:
            if self.conn:
                cursor = self.conn.cursor()
                cursor.close()
                self.conn.close()
                print("Database connection closed.")
        except Exception as e:
            print(f"Error closing database connection: {e}")
    
    def on_closing(self):
        """Method called when the window is being closed."""
        self.close_db_connection()
        self.root.destroy()

    def get_all_tables(self):
        """Fetch all table names from the database."""
        tables = []
        try:
            cursor = self.conn.cursor()
            # Query to get all user tables from the database
            cursor.execute("""
                SELECT TABLE_NAME 
                FROM INFORMATION_SCHEMA.TABLES 
                WHERE TABLE_TYPE = 'BASE TABLE' 
                AND TABLE_SCHEMA = 'dbo'
            """)
            tables = [row[0] for row in cursor.fetchall()]
        except Exception as e:
            messagebox.showerror("Error", f"Error fetching tables: {e}")
        finally:
            if cursor:
                cursor.close()
        return tables

    def create_table_selection(self):
        self.clear_frame()
        
        # Table selection frame
        table_frame = ttk.LabelFrame(self.main_frame, text="Select Table", padding="10")
        table_frame.grid(row=0, column=0, padx=5, pady=5)
        
        ttk.Button(table_frame, text="Table 1: Patient", 
                  command=lambda: self.show_operations_menu("Patient")).grid(row=0, column=0, pady=5)
        ttk.Button(table_frame, text="Table 2: HealthProvider", 
                  command=lambda: self.show_operations_menu("HealthProvider")).grid(row=1, column=0, pady=5)

    def show_operations_menu(self, table_name):
        self.clear_frame()
        self.current_table = table_name
        
        # Operations frame
        ops_frame = ttk.LabelFrame(self.main_frame, text=f"Operations for {table_name}", padding="10")
        ops_frame.grid(row=0, column=0, padx=5, pady=5)
        
        ttk.Button(ops_frame, text="Option 1: Select", 
                  command=lambda: self.show_select_options()).grid(row=0, column=0, pady=5)
        ttk.Button(ops_frame, text="Option 2: Insert", 
                  command=self.show_insert_form).grid(row=1, column=0, pady=5)
        ttk.Button(ops_frame, text="Option 3: Update", 
                  command=self.show_update_form).grid(row=2, column=0, pady=5)
        ttk.Button(ops_frame, text="Option 4: Delete", 
                  command=self.show_delete_form).grid(row=3, column=0, pady=5)
        
        ttk.Button(ops_frame, text="Back", 
                  command=self.create_table_selection).grid(row=4, column=0, pady=20)

    def show_select_options(self):
        self.clear_frame()
        
        select_frame = ttk.LabelFrame(self.main_frame, text="Select Options", padding="10")
        select_frame.grid(row=0, column=0, padx=5, pady=5)
        
        ttk.Button(select_frame, text="Simple Select", 
                  command=self.perform_simple_select).grid(row=0, column=0, pady=5)
        ttk.Button(select_frame, text="Join Select", 
                  command=self.perform_join_select).grid(row=1, column=0, pady=5)
        ttk.Button(select_frame, text="Generate Report", 
                  command=self.generate_report).grid(row=2, column=0, pady=5)
        ttk.Button(select_frame, text="Back", 
                  command=lambda: self.show_operations_menu(self.current_table)).grid(row=3, column=0, pady=20)

    def perform_simple_select(self):
        self.clear_frame()
        
        results_frame = ttk.LabelFrame(self.main_frame, text=f"{self.current_table} Records", padding="10")
        results_frame.grid(row=0, column=0, padx=5, pady=5)
        
        # Create Treeview
        columns = self.get_table_columns()
        tree = ttk.Treeview(results_frame, columns=columns, show="headings", height=15)
        
        # Set column headings
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=100)
        
        # Fetch and display data
        cursor = None
        try:
            cursor = self.conn.cursor()
            cursor.execute(f"SELECT * FROM {self.current_table}")
            for row in cursor.fetchall():
                tree.insert("", tk.END, values=list(row))
        except Exception as e:
            messagebox.showerror("Error", f"Error fetching records: {e}")
        finally:
            if cursor:
                cursor.close()
        
        # Add scrollbars
        y_scrollbar = ttk.Scrollbar(results_frame, orient="vertical", command=tree.yview)
        x_scrollbar = ttk.Scrollbar(results_frame, orient="horizontal", command=tree.xview)
        tree.configure(yscrollcommand=y_scrollbar.set, xscrollcommand=x_scrollbar.set)
        
        # Grid layout
        tree.grid(row=0, column=0, sticky="nsew")
        y_scrollbar.grid(row=0, column=1, sticky="ns")
        x_scrollbar.grid(row=1, column=0, sticky="ew")
        
        ttk.Button(results_frame, text="Back", 
                  command=self.show_select_options).grid(row=2, column=0, columnspan=2, pady=20)

    def perform_join_select(self):
        self.clear_frame()
        
        join_frame = ttk.LabelFrame(self.main_frame, text="Join Results", padding="10")
        join_frame.grid(row=0, column=0, padx=5, pady=5)
        
        if self.current_table == "Patient":
            query = """
                SELECT 
                    p.PatientID, p.Name as PatientName, 
                    hp.Name as ProviderName, hp.Specialty,
                    a.AppointmentID, a.Time, a.EmergencyStatus
                FROM Patient p
                JOIN Appointment a ON p.PatientID = a.PatientID
                JOIN HealthPoviderAppointments hpa ON a.AppointmentID = hpa.AppointmentID
                JOIN HealthProvider hp ON hpa.ProviderID = hp.ProviderID
            """
        else:  # HealthProvider
            query = """
                SELECT 
                    hp.ProviderID, hp.Name as ProviderName, hp.Specialty,
                    p.Name as PatientName, a.Time, a.EmergencyStatus
                FROM HealthProvider hp
                JOIN HealthPoviderAppointments hpa ON hp.ProviderID = hpa.ProviderID
                JOIN Appointment a ON hpa.AppointmentID = a.AppointmentID
                JOIN Patient p ON a.PatientID = p.PatientID
            """
        
        cursor = None
        try:
            cursor = self.conn.cursor()
            cursor.execute(query)
        
            # Create Treeview
            columns = [column[0] for column in cursor.description]
            tree = ttk.Treeview(join_frame, columns=columns, show="headings", height=15)
        
            # Set column headings
            for col in columns:
                tree.heading(col, text=col)
                tree.column(col, width=120)
        
            # Add data
            for row in cursor.fetchall():
                tree.insert("", tk.END, values=list(row))
        
        except Exception as e:
            messagebox.showerror("Error", f"Error fetching join data: {e}")
        finally:
            if cursor:
                cursor.close()

        # Add scrollbars
        y_scrollbar = ttk.Scrollbar(join_frame, orient="vertical", command=tree.yview)
        x_scrollbar = ttk.Scrollbar(join_frame, orient="horizontal", command=tree.xview)
        tree.configure(yscrollcommand=y_scrollbar.set, xscrollcommand=x_scrollbar.set)
        
        # Grid layout
        tree.grid(row=0, column=0, sticky="nsew")
        y_scrollbar.grid(row=0, column=1, sticky="ns")
        x_scrollbar.grid(row=1, column=0, sticky="ew")
        
        ttk.Button(join_frame, text="Back", 
                  command=self.show_select_options).grid(row=2, column=0, columnspan=2, pady=20)

    def generate_report(self):
        self.clear_frame()
        
        report_frame = ttk.LabelFrame(self.main_frame, text=f"Report for {self.current_table}", padding="10")
        report_frame.grid(row=0, column=0, padx=5, pady=5)
        
        if self.current_table == "Patient":
            query = """
                SELECT 
                    COUNT(*) as TotalPatients,
                    COUNT(CASE WHEN InsuranceStatus = 1 THEN 1 END) as InsuredPatients,
                    COUNT(CASE WHEN InsuranceStatus = 0 THEN 1 END) as UninsuredPatients,
                    AVG(Age) as AverageAge,
                    COUNT(DISTINCT InsuranceID) as UniqueInsuranceProviders
                FROM Patient
            """
        else:
            query = """
                SELECT 
                    COUNT(*) as TotalProviders,
                    COUNT(DISTINCT Specialty) as UniqueSpecialties,
                    COUNT(DISTINCT ProviderID) as ActiveProviders,
                    (SELECT COUNT(*) FROM HealthPoviderAppointments) as TotalAppointments
                FROM HealthProvider
            """
        
        cursor = self.conn.cursor()
        cursor.execute(query)
        result = cursor.fetchone()
        
        report_text = tk.Text(report_frame, height=15, width=60)
        report_text.insert(tk.END, f"Report Generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        
        for i, col in enumerate(cursor.description):
            report_text.insert(tk.END, f"{col[0]}: {result[i]}\n")
        
        report_text.config(state='disabled')
        report_text.grid(row=0, column=0, padx=5, pady=5)
        
        ttk.Button(report_frame, text="Back", 
                  command=self.show_select_options).grid(row=1, column=0, pady=20)
        
        if cursor:
            cursor.close()

    def show_insert_form(self):
        self.clear_frame()
        
        insert_frame = ttk.LabelFrame(self.main_frame, text=f"Insert {self.current_table}", padding="10")
        insert_frame.grid(row=0, column=0, padx=5, pady=5)
        
        # Create entry fields based on table columns
        self.entries = {}
        for i, column in enumerate(self.get_table_columns()):
            ttk.Label(insert_frame, text=column).grid(row=i, column=0, pady=2, padx=5, sticky="e")
            self.entries[column] = ttk.Entry(insert_frame, width=40)
            self.entries[column].grid(row=i, column=1, pady=2, padx=5, sticky="w")
        
        ttk.Button(insert_frame, text="Insert", 
                  command=self.perform_insert).grid(row=len(self.entries), column=0, columnspan=2, pady=20)
        ttk.Button(insert_frame, text="Back", 
                  command=lambda: self.show_operations_menu(self.current_table)).grid(row=len(self.entries)+1, column=0, columnspan=2)

    def perform_insert(self):
        values = [self.entries[column].get() for column in self.entries]
        columns = ", ".join(self.entries.keys())
        placeholders = ", ".join(["?" for _ in values])
        
        try:
            cursor = self.conn.cursor()
            cursor.execute(f"INSERT INTO {self.current_table} ({columns}) VALUES ({placeholders})", values)
            self.conn.commit()
            messagebox.showinfo("Success", "Record inserted successfully!")
            # Clear entries after successful insert
            for entry in self.entries.values():
                entry.delete(0, tk.END)
        except Exception as e:
            messagebox.showerror("Error", f"Error inserting record: {e}")
        finally:
            if cursor:
                cursor.close()

    def show_update_form(self):
        self.clear_frame()
        
        update_frame = ttk.LabelFrame(self.main_frame, text=f"Update {self.current_table}", padding="10")
        update_frame.grid(row=0, column=0, padx=5, pady=5)
        
        # ID Entry
        id_field = f"{self.current_table}ID"
        ttk.Label(update_frame, text=f"Enter {id_field} to update:").grid(row=0, column=0, pady=10)
        id_entry = ttk.Entry(update_frame, width=40)
        id_entry.grid(row=0, column=1, pady=10)
        
        ttk.Button(update_frame, text="Load Record", 
                  command=lambda: self.load_record_for_update(id_entry.get())).grid(row=1, column=0, columnspan=2, pady=10)
        
        # Create entry fields for update
        self.update_entries = {}
        columns = self.get_table_columns()[1:]  # Skip ID column
        for i, column in enumerate(columns, start=2):
            ttk.Label(update_frame, text=column).grid(row=i, column=0, pady=2, padx=5, sticky="e")
            self.update_entries[column] = ttk.Entry(update_frame, width=40)
            self.update_entries[column].grid(row=i, column=1, pady=2, padx=5, sticky="w")
        
        self.update_id = id_entry  # Store reference to ID entry
        
        ttk.Button(update_frame, text="Update", 
                  command=self.perform_update).grid(row=len(columns)+2, column=0, columnspan=2, pady=20)
        ttk.Button(update_frame, text="Back", 
                  command=lambda: self.show_operations_menu(self.current_table)).grid(row=len(columns)+3, column=0, columnspan=2)

    def load_record_for_update(self, record_id):
        if not record_id:
            messagebox.showerror("Error", "Please enter an ID")
            return
            
        try:
            cursor = self.conn.cursor()
            cursor.execute(f"SELECT * FROM {self.current_table} WHERE {self.current_table}ID = ?", record_id)
            record = cursor.fetchone()
            
            if record:
                # Fill entry fields with current values
                for i, (column, entry) in enumerate(self.update_entries.items(), start=1):
                    entry.delete(0, tk.END)
                    entry.insert(0, str(record[i]))
            else:
                messagebox.showerror("Error", "Record not found")
        except Exception as e:
            messagebox.showerror("Error", f"Error loading record: {e}")
        finally:
            if cursor:
                cursor.close()

    def perform_update(self):
        record_id = self.update_id.get()
        if not record_id:
            messagebox.showerror("Error", "Please provide an ID")
            return
        
        set_clause = ", ".join([f"{col} = ?" for col in self.update_entries.keys()])
        values = [self.update_entries[col].get() for col in self.update_entries.keys()]
        values.append(record_id)  # Add ID for WHERE clause
        
        try:
            cursor = self.conn.cursor()
            cursor.execute(
                f"UPDATE {self.current_table} SET {set_clause} WHERE {self.current_table}ID = ?",
                values
            )
            self.conn.commit()
            messagebox.showinfo("Success", "Record updated successfully!")
            # Clear entries after successful update
            for entry in self.update_entries.values():
                entry.delete(0, tk.END)
            self.update_id.delete(0, tk.END)
        except Exception as e:
            messagebox.showerror("Error", f"Error updating record: {e}")
        finally:
            if cursor:
                cursor.close()

    def show_delete_form(self):
        self.clear_frame()
        
        delete_frame = ttk.LabelFrame(self.main_frame, text=f"Delete from {self.current_table}", padding="10")
        delete_frame.grid(row=0, column=0, padx=5, pady=5)
        
        # Search frame for finding records to delete
        search_frame = ttk.Frame(delete_frame)
        search_frame.grid(row=0, column=0, padx=5, pady=5)
        
        ttk.Label(search_frame, text=f"{self.current_table}ID:").grid(row=0, column=0, padx=5)
        id_entry = ttk.Entry(search_frame)
        id_entry.grid(row=0, column=1, padx=5)
        
        # Create Treeview to show the record to be deleted
        columns = self.get_table_columns()
        self.delete_tree = ttk.Treeview(delete_frame, columns=columns, show="headings", height=5)
        
        # Set column headings
        for col in columns:
            self.delete_tree.heading(col, text=col)
            self.delete_tree.column(col, width=100)
        
        self.delete_tree.grid(row=1, column=0, padx=5, pady=5)
        
        # Buttons
        button_frame = ttk.Frame(delete_frame)
        button_frame.grid(row=2, column=0, pady=10)
        
        ttk.Button(button_frame, text="Find Record", 
                  command=lambda: self.find_record_for_delete(id_entry.get())).grid(row=0, column=0, padx=5)
        ttk.Button(button_frame, text="Delete Record", 
                  command=self.perform_delete).grid(row=0, column=1, padx=5)
        ttk.Button(button_frame, text="Back", 
                  command=lambda: self.show_operations_menu(self.current_table)).grid(row=0, column=2, padx=5)

    def find_record_for_delete(self, record_id):
        if not record_id:
            messagebox.showerror("Error", "Please enter an ID")
            return
            
        try:
            cursor = self.conn.cursor()
            cursor.execute(f"SELECT * FROM {self.current_table} WHERE {self.current_table}ID = ?", record_id)
            record = cursor.fetchone()
            
            # Clear existing items
            for item in self.delete_tree.get_children():
                self.delete_tree.delete(item)
            
            if record:
                self.delete_tree.insert("", tk.END, values=list(record))
            else:
                messagebox.showerror("Error", "Record not found")
        except Exception as e:
            messagebox.showerror("Error", f"Error finding record: {e}")
        finally:
            if cursor:
                cursor.close()

    def perform_delete(self):
        selected_item = self.delete_tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "Please find and select a record to delete")
            return
        
        record = self.delete_tree.item(selected_item[0])['values']
        if not record:
            return
            
        if messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this record?"):
            try:
                cursor = self.conn.cursor()
                cursor.execute(
                    f"DELETE FROM {self.current_table} WHERE {self.current_table}ID = ?", 
                    (record[0],)
                )
                self.conn.commit()
                
                # print(f"Current table: {self.current_table}")
                # print(f"ID column: {self.current_table}ID")
                # query = f"DELETE FROM {self.current_table} WHERE {self.current_table}ID = ?"
                # print(f"Executing query: {query} with parameter: {(record[0],)}")
                # print("Value to be deleted:", record[0])
                # print("Type:", type(record[0]))
                # print(record)
                # print(type(record))
                # for attr in record:
                #     print(attr)
                # print(self.delete_tree.item(selected_item[0]), '\n')
                # print(self.delete_tree.item(selected_item))

                # cursor = self.conn.cursor()
                # cursor.execute(query, (record[0],))
                # rows_deleted = cursor.rowcount
                # print(f"Rows deleted: {rows_deleted}")
                # self.conn.commit()
                
                messagebox.showinfo("Success", "Record deleted successfully!")
                # Clear the treeview
                for item in self.delete_tree.get_children():
                    self.delete_tree.delete(item)
            except Exception as e:
                # self.conn.rollback() # Important: Rollback on error
                messagebox.showerror("Error", f"Error deleting record: {e}")
            finally:
                if cursor:
                    cursor.close()

    def get_table_columns(self):
        if self.current_table == "Patient":
            return ["PatientID", "Name", "PhoneNo", "NationalID", "InsuranceStatus", 
                   "Birthdate", "Gender", "Email", "Age", "InsuranceID", "PackageID"]
        else:  # HealthProvider
            return ["ProviderID", "Availability", "Specialty", "Name"]

    def clear_frame(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()

    def generate_report(self):
        self.clear_frame()

        report_frame = ttk.LabelFrame(self.main_frame, text=f"Report for {self.current_table}", padding="10")
        report_frame.grid(row=0, column=0, padx=5, pady=5)

        try:
            cursor = self.conn.cursor()
            report_data = []
            column_names = []
            report_title = f"{self.current_table} Analysis Report"

            # Get basic statistics for any table
            cursor.execute(f"""
                SELECT 
                    COUNT(*) as TotalRecords,
                    COUNT(DISTINCT {self.get_table_columns()[0]}) as UniqueIDs
                FROM {self.current_table}
            """)
            basic_stats = cursor.fetchone()
            report_data.extend([basic_stats[0], basic_stats[1]])
            column_names.extend(['Total Records', 'Unique IDs'])

            # Add table-specific statistics
            if self.current_table == "Patient":
                cursor.execute("""
                    SELECT 
                        COUNT(CASE WHEN InsuranceStatus = 1 THEN 1 END) as InsuredPatients,
                        COUNT(CASE WHEN InsuranceStatus = 0 THEN 1 END) as UninsuredPatients,
                        AVG(Age) as AverageAge,
                        COUNT(DISTINCT InsuranceID) as UniqueInsuranceProviders
                    FROM Patient
                """)
                stats = cursor.fetchone()
                report_data.extend([stats[0], stats[1], stats[2], stats[3]])
                column_names.extend([
                    'Insured Patients',
                    'Uninsured Patients',
                    'Average Age',
                    'Unique Insurance Providers'
                ])
            elif self.current_table == "HealthProvider":
                cursor.execute("""
                    SELECT 
                        COUNT(DISTINCT Specialty) as UniqueSpecialties,
                        COUNT(CASE WHEN Availability = 1 THEN 1 END) as AvailableProviders
                    FROM HealthProvider
                """)
                stats = cursor.fetchone()
                report_data.extend([stats[0], stats[1]])
                column_names.extend(['Unique Specialties', 'Available Providers'])

            # Display report in text widget
            report_text = tk.Text(report_frame, height=15, width=60)
            report_text.insert(tk.END, f"Report Generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")

            for name, value in zip(column_names, report_data):
                if isinstance(value, float):
                    report_text.insert(tk.END, f"{name}: {value:.2f}\n")
                else:
                    report_text.insert(tk.END, f"{name}: {value}\n")

            report_text.config(state='disabled')
            report_text.grid(row=0, column=0, padx=5, pady=5)

            # Add Export to PDF button
            def export_to_pdf():
                file_path = filedialog.asksaveasfilename(
                    defaultextension=".pdf",
                    filetypes=[("PDF files", "*.pdf")],
                    initialfile=f"{self.current_table}_report.pdf"
                )
                if file_path:
                    self.generate_pdf_report(report_title, report_data, column_names, file_path)

            button_frame = ttk.Frame(report_frame)
            button_frame.grid(row=1, column=0, pady=10)

            ttk.Button(button_frame, text="Export to PDF",
                       command=export_to_pdf).grid(row=0, column=0, padx=5)
            ttk.Button(button_frame, text="Back",
                       command=self.show_select_options).grid(row=0, column=1, padx=5)

        except Exception as e:
            messagebox.showerror("Error", f"Error generating report: {e}")
        finally:
            if cursor:
                cursor.close()

    def generate_pdf_report(self, report_title, report_data, column_names, output_file_path):
        """Generate and save a PDF report with charts."""
        try:
            # Create the PDF canvas
            c = canvas.Canvas(output_file_path, pagesize=letter)
            c.setFont("Helvetica-Bold", 16)

            # Add title
            c.drawString(100, 750, report_title)

            # Add timestamp
            c.setFont("Helvetica", 12)
            c.drawString(100, 730, f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

            # Add line separator
            c.line(100, 720, 500, 720)

            # Write the report data
            y = 700
            for col, value in zip(column_names, report_data):
                if isinstance(value, float):
                    formatted_value = f"{value:.2f}"
                else:
                    formatted_value = str(value)
                c.drawString(100, y, f"{col}: {formatted_value}")
                y -= 20

            # Generate and add charts based on table type
            if self.current_table == "Patient":
                # Create pie chart for insurance status
                self.add_insurance_status_chart(c, report_data, column_names)

                # Create bar chart for age distribution
                self.add_age_distribution_chart(c)

            elif self.current_table == "HealthProvider":
                # Create pie chart for specialties distribution
                self.add_specialty_distribution_chart(c)

                # Create bar chart for provider availability
                self.add_provider_availability_chart(c)

            # Save the PDF
            c.save()
            messagebox.showinfo("Success", f"Report saved successfully to:\n{output_file_path}")

        except Exception as e:
            messagebox.showerror("Error", f"Failed to create PDF: {e}")

    def add_insurance_status_chart(self, pdf_canvas, report_data, column_names):
        """Add insurance status pie chart to PDF."""
        try:
            # Get insurance data from report_data
            insured_idx = column_names.index('Insured Patients')
            uninsured_idx = column_names.index('Uninsured Patients')

            insured = report_data[insured_idx]
            uninsured = report_data[uninsured_idx]

            # Create pie chart
            plt.figure(figsize=(6, 4))
            plt.pie([insured, uninsured],
                    labels=['Insured', 'Uninsured'],
                    autopct='%1.1f%%',
                    colors=['lightblue', 'lightcoral'])
            plt.title('Insurance Status Distribution')

            # Save chart to bytes buffer
            buf = io.BytesIO()
            plt.savefig(buf, format='png', bbox_inches='tight')
            plt.close()

            # Add chart to PDF
            buf.seek(0)
            img = ImageReader(buf)
            pdf_canvas.drawImage(img, 100, 400, width=4 * inch, height=3 * inch)

        except Exception as e:
            print(f"Error creating insurance status chart: {e}")

    def add_age_distribution_chart(self, pdf_canvas):
        """Add age distribution chart to PDF."""
        try:
            cursor = self.conn.cursor()
            cursor.execute("""
                SELECT 
                    CASE 
                        WHEN Age < 18 THEN '0-17'
                        WHEN Age BETWEEN 18 AND 30 THEN '18-30'
                        WHEN Age BETWEEN 31 AND 50 THEN '31-50'
                        WHEN Age BETWEEN 51 AND 70 THEN '51-70'
                        ELSE '70+'
                    END as AgeGroup,
                    COUNT(*) as Count
                FROM Patient
                GROUP BY 
                    CASE 
                        WHEN Age < 18 THEN '0-17'
                        WHEN Age BETWEEN 18 AND 30 THEN '18-30'
                        WHEN Age BETWEEN 31 AND 50 THEN '31-50'
                        WHEN Age BETWEEN 51 AND 70 THEN '51-70'
                        ELSE '70+'
                    END
                ORDER BY AgeGroup
            """)

            age_groups, counts = zip(*cursor.fetchall())

            plt.figure(figsize=(6, 4))
            plt.bar(age_groups, counts, color='skyblue')
            plt.title('Age Distribution')
            plt.xlabel('Age Groups')
            plt.ylabel('Number of Patients')
            plt.xticks(rotation=45)

            # Save chart to bytes buffer
            buf = io.BytesIO()
            plt.savefig(buf, format='png', bbox_inches='tight')
            plt.close()

            # Add chart to PDF
            buf.seek(0)
            img = ImageReader(buf)
            pdf_canvas.drawImage(img, 100, 100, width=4 * inch, height=3 * inch)

        except Exception as e:
            print(f"Error creating age distribution chart: {e}")
        finally:
            if cursor:
                cursor.close()

    def add_specialty_distribution_chart(self, pdf_canvas):
        """Add specialty distribution chart to PDF."""
        try:
            cursor = self.conn.cursor()
            cursor.execute("""
                SELECT Specialty, COUNT(*) as Count
                FROM HealthProvider
                GROUP BY Specialty
                ORDER BY Count DESC
            """)

            specialties, counts = zip(*cursor.fetchall())

            plt.figure(figsize=(6, 4))
            plt.pie(counts, labels=specialties, autopct='%1.1f%%')
            plt.title('Provider Specialty Distribution')

            # Save chart to bytes buffer
            buf = io.BytesIO()
            plt.savefig(buf, format='png', bbox_inches='tight')
            plt.close()

            # Add chart to PDF
            buf.seek(0)
            img = ImageReader(buf)
            pdf_canvas.drawImage(img, 100, 400, width=4 * inch, height=3 * inch)

        except Exception as e:
            print(f"Error creating specialty distribution chart: {e}")
        finally:
            if cursor:
                cursor.close()

    def add_provider_availability_chart(self, pdf_canvas):
        """Add provider availability chart to PDF."""
        try:
            cursor = self.conn.cursor()
            cursor.execute("""
                SELECT 
                    Specialty,
                    SUM(CASE WHEN Availability = 1 THEN 1 ELSE 0 END) as Available,
                    SUM(CASE WHEN Availability = 0 THEN 1 ELSE 0 END) as Unavailable
                FROM HealthProvider
                GROUP BY Specialty
            """)

            data = cursor.fetchall()
            specialties = [row[0] for row in data]
            available = [row[1] for row in data]
            unavailable = [row[2] for row in data]

            x = np.arange(len(specialties))
            width = 0.35

            plt.figure(figsize=(8, 4))
            plt.bar(x - width / 2, available, width, label='Available', color='lightgreen')
            plt.bar(x + width / 2, unavailable, width, label='Unavailable', color='lightcoral')

            plt.xlabel('Specialty')
            plt.ylabel('Number of Providers')
            plt.title('Provider Availability by Specialty')
            plt.xticks(x, specialties, rotation=45)
            plt.legend()
            plt.tight_layout()

            # Save chart to bytes buffer
            buf = io.BytesIO()
            plt.savefig(buf, format='png', bbox_inches='tight')
            plt.close()

            # Add chart to PDF
            buf.seek(0)
            img = ImageReader(buf)
            pdf_canvas.drawImage(img, 100, 100, width=4 * inch, height=3 * inch)

        except Exception as e:
            print(f"Error creating provider availability chart: {e}")
        finally:
            if cursor:
                cursor.close()

if __name__ == "__main__":
    root = tk.Tk()
    app = HealthNetworkApp(root)
    root.mainloop()