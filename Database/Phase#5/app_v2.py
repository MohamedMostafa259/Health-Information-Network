import io
import tkinter as tk
from tkinter import ttk, messagebox, filedialog

import numpy as np
# import pandas as pd
import pyodbc
from datetime import datetime
from reportlab.lib.units import inch
from matplotlib import pyplot as plt
import seaborn as sns
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
                # server name
                r"Server=Mohamed_Mostafa\SQLEXPRESS;"  # Mohamed Mostafa  → r"Server=Mohamed_Mostafa\SQLEXPRESS;" 
                                                       # Mohamed Ibrahim → r"Server=MOHAMED\MSSQLSERVER01;"
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

        tables = ["Patient", "HealthProvider", "GovernmentRegulator", "InsuranceCompany",
                  "Package", "PackageDetails", "InsuranceCompanyPackages", "Report",
                  "GovernmentRegulatorReports", "Appointment", "HealthPoviderAppointments", 
                  "HealthRecord", "Regulator_Access_HealthRecord", "Notification", 
                  "ReportGeneration", "Card", "Caregiver", "CaregiversNotifications"]

        for i, table in enumerate(tables):
            ttk.Button(table_frame, text=f"Table {i + 1}: {table}", 
                       command=lambda t=table: self.show_operations_menu(t)).grid(row=i, column=0, pady=5)
        
    def show_operations_menu(self, table_name):
        self.clear_frame()
        self.current_table = table_name

        # Operations frame
        ops_frame = ttk.LabelFrame(self.main_frame, text=f"Operations for {table_name}", padding="10")
        ops_frame.grid(row=0, column=0, padx=5, pady=5)

        ttk.Button(ops_frame, text="Select", 
                   command=self.show_select_options).grid(row=0, column=0, pady=5)
        ttk.Button(ops_frame, text="Insert", 
                   command=self.show_insert_form).grid(row=1, column=0, pady=5)
        ttk.Button(ops_frame, text="Update", 
                   command=self.show_update_form).grid(row=2, column=0, pady=5)
        ttk.Button(ops_frame, text="Delete", 
                   command=self.show_delete_form).grid(row=3, column=0, pady=5)
        ttk.Button(ops_frame, text="Join Select", 
                  command=self.perform_join_select).grid(row=4, column=0, pady=5)
        ttk.Button(ops_frame, text="Back", 
                   command=self.create_table_selection).grid(row=5, column=0, pady=20)

    def show_select_options(self):
        self.clear_frame()
        
        select_frame = ttk.LabelFrame(self.main_frame, text="Select Options", padding="10")
        select_frame.grid(row=0, column=0, padx=5, pady=5)
        
        ttk.Button(select_frame, text="Simple Select", 
                  command=self.perform_simple_select).grid(row=0, column=0, pady=5)
        ttk.Button(select_frame, text="Custom Select", 
                   command=self.show_custom_select_form).grid(row=1, column=0, pady=5)
        # ttk.Button(select_frame, text="Join Select", 
        #           command=self.perform_join_select).grid(row=2, column=0, pady=5)
        ttk.Button(select_frame, text="Generate Report", 
                  command=self.generate_report).grid(row=3, column=0, pady=5)
        ttk.Button(select_frame, text="Back", 
                  command=lambda: self.show_operations_menu(self.current_table)).grid(row=4, column=0, pady=20)

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

    def show_custom_select_form(self):
        self.clear_frame()

        select_frame = ttk.LabelFrame(self.main_frame, text=f"Custom Select for {self.current_table}", padding="10")
        select_frame.grid(row=0, column=0, padx=5, pady=5)

        # Checkboxes for columns
        self.selected_columns = []
        columns = self.get_table_columns()

        ttk.Label(select_frame, text="Select Columns:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        for i, col in enumerate(columns):
            var = tk.BooleanVar()
            chk = ttk.Checkbutton(select_frame, text=col, variable=var)
            chk.grid(row=i+1, column=0, sticky="w", padx=5, pady=2)
            self.selected_columns.append((col, var))

        # Execute button
        ttk.Button(select_frame, text="Execute", 
                   command=self.perform_custom_select).grid(row=len(columns)+1, column=0, pady=10)
        ttk.Button(select_frame, text="Back", 
                   command=self.show_select_options).grid(row=len(columns)+2, column=0, pady=10)

    def perform_custom_select(self):
        columns_to_select = [col for col, var in self.selected_columns if var.get()]
        if not columns_to_select:
            messagebox.showerror("Error", "Please select at least one column.")
            return

        self.clear_frame()

        results_frame = ttk.LabelFrame(self.main_frame, text=f"Custom Select Results for {self.current_table}", padding="10")
        results_frame.grid(row=0, column=0, padx=5, pady=5)

        # Create Treeview
        tree = ttk.Treeview(results_frame, columns=columns_to_select, show="headings", height=15)

        # Set column headings
        for col in columns_to_select:
            tree.heading(col, text=col)
            tree.column(col, width=100)

        # Fetch and display data
        cursor = None
        try:
            cursor = self.conn.cursor()
            query = f"SELECT {', '.join(columns_to_select)} FROM {self.current_table}"
            cursor.execute(query)
            for row in cursor.fetchall():
                tree.insert("", tk.END, values=list(row))
        except Exception as e:
            messagebox.showerror("Error", f"Error fetching custom select records: {e}")
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
                   command=self.show_custom_select_form).grid(row=2, column=0, columnspan=2, pady=20)



    def perform_join_select(self):
        self.clear_frame()

        join_frame = ttk.LabelFrame(self.main_frame, text="Dynamic Join Selector", padding="10")
        join_frame.grid(row=0, column=0, padx=5, pady=5)

        # Dropdowns for table and join type selection
        tables = self.get_all_tables()
        join_types = ["INNER JOIN", "LEFT JOIN", "RIGHT JOIN", "FULL JOIN"]

        def table_field(table_num, row):
            ttk.Label(join_frame, text=f"Table {table_num}:").grid(row=row, column=0, sticky="w")
            table_var = tk.StringVar()
            table_menu = ttk.OptionMenu(join_frame, table_var, None, *tables)
            table_var.set("Select a Table")  
            table_menu.grid(row=row, column=1, sticky="ew")
            return table_var

        def column_selection(row, table_var):
            # Column selection for Table 1
            ttk.Label(join_frame, text=f"Select Columns:").grid(row=row, column=2, sticky="w", padx=(20,0))
            table_cols_frame = ttk.Frame(join_frame)
            table_cols_frame.grid(row=row, column=3, sticky="w")
            table_col_vars = []

            def update_table_columns(*args):
                for widget in table_cols_frame.winfo_children():
                    widget.destroy()
                table_col_vars.clear()
                
                if table_var.get() != "Select a Table":
                    all_var = tk.BooleanVar(value=True)
                    ttk.Checkbutton(table_cols_frame, text="All", variable=all_var).pack(side=tk.LEFT)
                    table_col_vars.append(("All", all_var))

                    cursor = self.conn.cursor()
                    cursor.execute(f"SELECT TOP 1 * FROM {table_var.get()}")
                    columns = [description[0] for description in cursor.description]
                    cursor.close()

                    for col in columns:
                        var = tk.BooleanVar()
                        ttk.Checkbutton(table_cols_frame, text=col, variable=var).pack(side=tk.LEFT)
                        table_col_vars.append((col, var))

            table_var.trace('w', update_table_columns)
            return table_col_vars
           
        def join_field(row):
            ttk.Label(join_frame, text="Join Type:").grid(row=row, column=0, sticky="w")
            join_type_var = tk.StringVar()
            join_type_menu = ttk.OptionMenu(join_frame, join_type_var, None, *join_types)
            join_type_var.set(join_types[0])  # Explicitly set INNER JOIN
            join_type_menu.grid(row=row, column=1, sticky="ew")
            return join_type_var

        def condition_field(leftTableIdx, rightTableIdx, row):
            ttk.Label(join_frame, text=f"On Condition (e.g., table{leftTableIdx}.col = table{rightTableIdx}.col):").grid(row=row, column=0, sticky="w")
            on_condition_entry = ttk.Entry(join_frame, width=50)
            on_condition_entry.grid(row=row, column=1, sticky="ew")
            return on_condition_entry


        cur_row = 0
        cur_table_idx = 1

        self.table1 = table_field(table_num=cur_table_idx, row=cur_row)
        self.table1_selected_cols = column_selection(row=cur_row, table_var=self.table1); cur_table_idx += 1; cur_row += 1
        self.join1 = join_field(row=cur_row); cur_row += 1
        self.table2 = table_field(table_num=cur_table_idx, row=cur_row)
        self.table2_selected_cols = column_selection(row=cur_row, table_var=self.table2); cur_table_idx += 1; cur_row += 1
        self.on_condition1 = condition_field(leftTableIdx=1, rightTableIdx=2, row=cur_row); cur_row += 1

        self.join2 = join_field(row=cur_row); cur_row += 1
        self.table3 = table_field(table_num=cur_table_idx, row=cur_row)
        self.table3_selected_cols = column_selection(row=cur_row, table_var=self.table3); cur_table_idx += 1; cur_row += 1
        self.on_condition2 = condition_field(leftTableIdx=2, rightTableIdx=3, row=cur_row); cur_row += 1

        self.join3 = join_field(row=cur_row); cur_row += 1
        self.table4 = table_field(table_num=cur_table_idx, row=cur_row)
        self.table4_selected_cols = column_selection(row=cur_row, table_var=self.table4); cur_table_idx += 1; cur_row += 1
        self.on_condition3 = condition_field(leftTableIdx=3, rightTableIdx=4, row=cur_row); cur_row += 1

        def get_selected_columns(table_name, col_vars):
            selected_cols = []
            if col_vars[0][1].get(): # All is selected
                selected_cols = [f"{table_name}.*"]
            else:
                selected_cols = [f"{table_name}.{col}" for col, checked in col_vars if col != 'All' and checked.get()]
            return selected_cols

        def execute_join():
            if self.table1.get() == "Select a Table" or self.table2.get() == "Select a Table" or self.on_condition1.get() == "":
                messagebox.showerror("Error", "You should join at least two tables (fill the first 4 fields)")
                return

            table1_selected_cols = get_selected_columns(self.table1.get(), self.table1_selected_cols)
            table2_selected_cols = get_selected_columns(self.table2.get(), self.table2_selected_cols)
            tables_selected_cols = table1_selected_cols + table2_selected_cols

            query_joined_tables_part = f"{self.table1.get()} {self.join1.get()} {self.table2.get()} ON {self.on_condition1.get()}"
            # query_ON_part = self.on_condition1.get()
            
            if self.table3.get() != "Select a Table" and self.on_condition2.get() != "":
                query_joined_tables_part += f" {self.join2.get()} {self.table3.get()} ON {self.on_condition2.get()}"
                # query_ON_part += f" AND {self.on_condition2.get()}"
                table3_selected_cols = get_selected_columns(self.table3.get(), self.table3_selected_cols)
                tables_selected_cols += table3_selected_cols
            
                if self.table4.get() != "Select a Table" and self.on_condition3.get() != "":
                    print("table 4")
                    query_joined_tables_part += f" {self.join3.get()} {self.table4.get()} ON {self.on_condition3.get()}"
                    # query_ON_part += f" AND {self.on_condition3.get()}"
                    table4_selected_cols = get_selected_columns(self.table4.get(), self.table4_selected_cols)
                    tables_selected_cols += table4_selected_cols

            query_selected_columns_part = ', '.join(tables_selected_cols)

            # Execute join query
            try:
                cursor = self.conn.cursor()
                query = f"SELECT {query_selected_columns_part} FROM {query_joined_tables_part}"
                cursor.execute(query)
                print(query)

                # Display results
                columns = [desc[0] for desc in cursor.description]
                print(columns) ##############
                results_frame = ttk.Frame(join_frame)
                results_frame.grid(row=5, column=0, columnspan=2, sticky="nsew")

                tree = ttk.Treeview(results_frame, columns=columns, show="headings", height=15)
                for col in columns:
                    tree.heading(col, text=col)
                    tree.column(col, width=120)
                for row in cursor.fetchall():
                    tree.insert("", tk.END, values=list(row))

                y_scrollbar = ttk.Scrollbar(results_frame, orient="vertical", command=tree.yview)
                x_scrollbar = ttk.Scrollbar(results_frame, orient="horizontal", command=tree.xview)
                tree.configure(yscrollcommand=y_scrollbar.set, xscrollcommand=x_scrollbar.set)
                tree.grid(row=0, column=0, sticky="nsew")
                y_scrollbar.grid(row=0, column=1, sticky="ns")
                x_scrollbar.grid(row=1, column=0, sticky="ew")

            except Exception as e:
                messagebox.showerror("Error", f"Error executing join query: {e}")

        # Execute button
        ttk.Button(join_frame, text="Execute Join", command=execute_join).grid(row=10, column=0, columnspan=2, pady=10)

        # Back button
        ttk.Button(join_frame, text="Back", command=lambda: self.show_operations_menu(self.current_table)).grid(row=cur_row + 1, column=0, columnspan=2, pady=10)

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
        table_columns = {
            "Patient": ["PatientID", "Name", "PhoneNo", "NationalID", "InsuranceStatus", 
                        "Birthdate", "Gender", "Email", "Age", "InsuranceID", "PackageID"],

            "HealthProvider": ["ProviderID", "Availability", "Specialty", "Name"],
            
            "GovernmentRegulator": ["RegulatorID", "Name", "Position"],
            
            "InsuranceCompany": ["InsuranceID", "CompanyName", "Email", "Phone"],
            
            "Package": ["PackageID"],
            
            "PackageDetails": ["IllnessType", "Percentage", "PackageID"],
            
            "InsuranceCompanyPackages": ["InsuranceID", "PackageID"],
            
            "Report": ["ReportID", "ReportType", "GenerateDate"],
            
            "GovernmentRegulatorReports": ["ReportID", "RegulatorID"],
            
            "Appointment": ["AppointmentID", "EmergencyStatus", "Time", "Type_of_illness", "PaymentAmount", 
                             "PaymentMethod", "PatientID"],
            
            "HealthPoviderAppointments": ["AppointmentID", "ProviderID"],

            "HealthRecord": ["RecordID", "TypeOfIncident", "DateOfIncident", "Details", "PatientID", 
                             "AppointmentID", "ProviderID"],
            
            "Regulator_Access_HealthRecord": ["RegulatorID", "RecordID"],
            
            "Notification": ["NotificationID", "Message", "NotificationType", "Date", "PatientID", 
                              "InsuranceID", "AppointmentID"],
            
            "ReportGeneration": ["NotificationID", "ProviderID", "ReportID"],
            
            "Card": ["CardNumber", "ExpirationDate", "CardHolderName", "CardType", "BankName", "PatientID"],
            
            "Caregiver": ["PatientID", "Relationship", "Name", "Phone", "Email"],
            
            "CaregiversNotifications": ["Relationship", "Name", "NotificationID", "PatientID"]
        }
        return table_columns.get(self.current_table, [])

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
                    COUNT(*) as TotalRecords
                FROM {self.current_table}
            """)
            total_records = cursor.fetchone()
            report_data.extend([total_records[0]])
            column_names.extend([f'Total {self.current_table}s'])

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
                    SELECT COUNT(DISTINCT Specialty)
                    FROM HealthProvider
                """)
                num_unique_specialties = cursor.fetchone()
                report_data.extend([num_unique_specialties[0]])
                column_names.extend(['Unique Specialties'])

                cursor.execute("""
                    SELECT DISTINCT Specialty
                    FROM HealthProvider
                """)
                # print(cursor.fetchone())
                specialties = cursor.fetchall()
                for idx, specialty in enumerate(specialties):
                    report_data.extend([specialty[0]])
                    column_names.extend([f'     Specialty {idx+1}'])

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
            plt.title('Health Provider Specialty Distribution')

            # Save chart to bytes buffer
            buf = io.BytesIO()
            plt.savefig(buf, format='png', bbox_inches='tight')
            plt.close()

            # Add chart to PDF
            buf.seek(0)
            img = ImageReader(buf)
            pdf_canvas.drawImage(img, x=100, y=350, width=4 * inch, height=3 * inch)

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
                SELECT Specialty, Availability
                FROM HealthProvider
            """)

            data = cursor.fetchall()
            specialties = [row[0] for row in data]
            availabilities = [row[1] for row in data]
            print(specialties)
            print(availabilities)

            plt.figure(figsize=(8, 6))
            sns.countplot(x=availabilities, hue=specialties)

            plt.xlabel('Specialty')
            plt.ylabel('Number of Providers')
            plt.title('Health Provider Availability by Specialty')
            plt.xticks(rotation=45)
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
            print(f"Error creating Health Provider Specialties chart: {e}")
        finally:
            if cursor:
                cursor.close()

if __name__ == "__main__":
    root = tk.Tk()
    app = HealthNetworkApp(root)
    root.mainloop()
