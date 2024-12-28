import tkinter as tk
from tkinter import ttk, messagebox
import pyodbc
from datetime import datetime
import subprocess
import platform
import re


class HealthNetworkApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Health Information Network Management System")
        self.root.geometry("1200x700")

        # Initialize connection and cursor
        self.conn = None
        self.cursor = None

        # Initialize other variables
        self.current_table = None
        self.entries = {}
        self.update_entries = {}
        self.delete_tree = None

        # Create main frame
        self.main_frame = ttk.Frame(self.root, padding="10")
        self.main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Configure grid weights
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

        # Server selection components
        self.server_var = tk.StringVar()
        self.create_server_selection()

        # Initialize table selection
        self.create_table_selection()

        # Bind the close event
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def create_server_selection(self):
        """Create the server selection interface"""
        server_frame = ttk.LabelFrame(self.main_frame, text="Server Connection", padding="5")
        server_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), padx=5, pady=5)

        ttk.Label(server_frame, text="Available Servers:").grid(row=0, column=0, sticky=tk.W, padx=5)

        self.server_menu = ttk.OptionMenu(server_frame, self.server_var, "")
        self.server_menu.grid(row=0, column=1, sticky=tk.W, padx=5)

        ttk.Button(server_frame, text="Refresh", command=self.on_refresh).grid(row=0, column=2, padx=5)
        ttk.Button(server_frame, text="Connect", command=self.on_connect).grid(row=0, column=3, padx=5)

        # Initialize server list
        self.on_refresh()

    def list_sql_servers(self):
        """
        Lists available SQL Server instances using multiple detection methods.
        Returns a list of server names.
        """
        servers = set()  # Use set to avoid duplicates

        try:
            # Method 1: Try using pyodbc's built-in driver enumeration
            drivers = [driver for driver in pyodbc.drivers() if 'SQL Server' in driver]
            if drivers:
                try:
                    # Get local machine name
                    local_machine = platform.node()
                    servers.add(local_machine + "\\SQLEXPRESS")
                    servers.add(local_machine)
                    servers.add("localhost")
                    servers.add("(local)")
                except Exception as e:
                    print(f"Error getting machine name: {e}")

            # Method 2: Try using sqlcmd if available
            # try:
            #     result = subprocess.run(
            #         ['sqlcmd', '-L'],
            #         stdout=subprocess.PIPE,
            #         stderr=subprocess.PIPE,
            #         text=True,
            #         timeout=5  # 5 second timeout
            #     )
            #     if result.returncode == 0:
            #         # Parse sqlcmd output and add valid server names
            #         for line in result.stdout.split('\n'):
            #             line = line.strip()
            #             # Match common SQL Server instance patterns
            #             if re.match(r'^[\w\-]+\\[\w\-_]+$', line) or \
            #                     re.match(r'^[\w\-]+$', line) or \
            #                     '\\' in line or \
            #                     line.lower() in ['localhost', '(local)']:
            #                 servers.add(line)
            # except (subprocess.TimeoutExpired, subprocess.SubprocessError, FileNotFoundError) as e:
            #     print(f"sqlcmd error: {e}")

            # Method 3: Try registry lookup (Windows only)
            if platform.system() == 'Windows':
                try:
                    import winreg
                    path = r"SOFTWARE\Microsoft\Microsoft SQL Server"
                    try:
                        reg_key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, path)
                        for i in range(winreg.QueryInfoKey(reg_key)[0]):
                            try:
                                instance_path = winreg.EnumKey(reg_key, i)
                                if instance_path.startswith('MSSQL'):
                                    # Extract instance name from registry
                                    instance_key = winreg.OpenKey(reg_key,
                                                                  instance_path + "\\MSSQLServer\\SuperSocketNetLib\\Tcp")
                                    instance_name = winreg.QueryValueEx(instance_key, 'TcpPort')[0]
                                    if instance_name:
                                        servers.add(f"{local_machine}\\{instance_name}")
                            except WindowsError:
                                continue
                    except WindowsError as e:
                        print(f"Registry error: {e}")
                except ImportError:
                    print("Failed to import winreg module")

            # Convert set to sorted list
            server_list = sorted(list(servers))

            # Validate servers are accessible
            validated_servers = []
            for server in server_list:
                try:
                    # Attempt a quick connection to verify server exists
                    conn_str = f"Driver={{SQL Server}};Server={server};Trusted_Connection=yes;Connection Timeout=3;"
                    conn = pyodbc.connect(conn_str, timeout=3)
                    conn.close()
                    validated_servers.append(server)
                except pyodbc.Error:
                    continue  # Skip servers that can't be connected to

            if not validated_servers:
                # If no servers were validated, add some default options
                validated_servers = ["localhost", "(local)", "localhost\\SQLEXPRESS"]

            return validated_servers

        except Exception as e:
            messagebox.showerror("Error", f"Error detecting SQL Servers: {e}")
            return ["localhost", "(local)", "localhost\\SQLEXPRESS"]  # Return default options on error

    def on_refresh(self):
        """Refresh server list"""
        servers = self.list_sql_servers()
        menu = self.server_menu['menu']
        menu.delete(0, 'end')

        if servers:
            for server in servers:
                menu.add_command(label=server,
                                 command=lambda s=server: self.server_var.set(s))
            self.server_var.set(servers[0])
        else:
            self.server_var.set("")
            messagebox.showinfo("No Servers", "No SQL Server instances found")

    def on_connect(self):
        """Handle server connection"""
        server = self.server_var.get()
        if not server:
            messagebox.showwarning("No Selection", "Please select a server")
            return

        try:
            # Close existing connection and cursor
            self.close_cursor()
            if self.conn:
                self.conn.close()

            connection_string = (
                f"Driver={{SQL Server}};"
                f"Server={server};"
                f"Database=HIN;"
                f"Trusted_Connection=yes;"
            )
            self.conn = pyodbc.connect(connection_string)

            # Create initial cursor
            if self.create_cursor():
                messagebox.showinfo("Success", f"Connected to {server}")
                self.create_table_selection()
            else:
                raise Exception("Failed to create cursor")

        except Exception as e:
            messagebox.showerror("Connection Error", f"Failed to connect: {e}")

    def create_table_selection(self):
        """Create the table selection interface"""
        self.clear_frame()

        table_frame = ttk.LabelFrame(self.main_frame, text="Select Table", padding="10")
        table_frame.grid(row=1, column=0, sticky=(tk.W, tk.E), padx=5, pady=5)

        for i, table in enumerate(["Patient", "HealthProvider"]):
            ttk.Button(table_frame,
                       text=f"Table {i + 1}: {table}",
                       command=lambda t=table: self.show_operations_menu(t)
                       ).grid(row=i, column=0, pady=5, padx=5, sticky=(tk.W, tk.E))

    def show_operations_menu(self, table_name):
        """Show operations menu for selected table"""
        self.clear_frame()
        self.current_table = table_name

        ops_frame = ttk.LabelFrame(self.main_frame, text=f"Operations for {table_name}", padding="10")
        ops_frame.grid(row=1, column=0, sticky=(tk.W, tk.E), padx=5, pady=5)

        operations = [
            ("Select", self.show_select_options),
            ("Insert", self.show_insert_form),
            ("Update", self.show_update_form),
            ("Delete", self.show_delete_form)
        ]

        for i, (op_name, op_func) in enumerate(operations):
            ttk.Button(ops_frame,
                       text=f"Option {i + 1}: {op_name}",
                       command=op_func
                       ).grid(row=i, column=0, pady=5, padx=5, sticky=(tk.W, tk.E))

        ttk.Button(ops_frame,
                   text="Back",
                   command=self.create_table_selection
                   ).grid(row=len(operations), column=0, pady=20, sticky=(tk.W, tk.E))

    def close_db_connection(self):
        """Close database connection and cursor"""
        self.close_cursor()
        try:
            if self.conn:
                self.conn.close()
                self.conn = None
                print("Database connection closed")
        except Exception as e:
            print(f"Error closing connection: {e}")
    
    def on_closing(self):
        """Handle application closing"""
        self.close_db_connection()
        self.root.destroy()

    def create_table_selection(self):
        self.clear_frame()
        
        # Table selection frame
        table_frame = ttk.LabelFrame(self.main_frame, text="Select Table", padding="10")
        table_frame.grid(row=0, column=0, padx=5, pady=5)
        
        ttk.Button(table_frame, text="Table 1: Patient", 
                  command=lambda: self.show_operations_menu("Patient")).grid(row=0, column=0, pady=5)
        ttk.Button(table_frame, text="Table 2: HealthProvider", 
                  command=lambda: self.show_operations_menu("HealthProvider")).grid(row=1, column=0, pady=5)


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

    def configure_treeview(self, parent, columns):
        tree = ttk.Treeview(parent, columns=columns, show="headings", height=15)
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=120)

        y_scrollbar = ttk.Scrollbar(parent, orient="vertical", command=tree.yview)
        x_scrollbar = ttk.Scrollbar(parent, orient="horizontal", command=tree.xview)
        tree.configure(yscrollcommand=y_scrollbar.set, xscrollcommand=x_scrollbar.set)

        tree.grid(row=0, column=0, sticky="nsew")
        y_scrollbar.grid(row=0, column=1, sticky="ns")
        x_scrollbar.grid(row=1, column=0, sticky="ew")
        return tree

    def perform_simple_select(self):
        self.clear_frame()

        results_frame = ttk.LabelFrame(self.main_frame, text=f"{self.current_table} Records", padding="10")
        results_frame.grid(row=0, column=0, padx=5, pady=5)

        # Create Treeview
        columns = self.get_table_columns()
        tree = self.configure_treeview(results_frame, columns)

        # Execute query
        cursor = self.execute_query(f"SELECT * FROM {self.current_table}")
        if cursor:
            try:
                for row in cursor.fetchall():
                    tree.insert("", tk.END, values=list(row))
            except Exception as e:
                messagebox.showerror("Error", f"Error fetching records: {e}")
            finally:
                self.close_cursor()

        ttk.Button(results_frame, text="Back",
                   command=self.show_select_options).grid(row=2, column=0, pady=20)

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
            tree = self.configure_treeview(join_frame, columns)
        
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
                    (SELECT COUNT(*) FROM HealthProviderAppointments) as TotalAppointments
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

    def execute_query(self, query, params=None):
        """Execute a query with proper cursor management"""
        try:
            if not self.create_cursor():
                raise Exception("No database connection")

            if params:
                self.cursor.execute(query, params)
            else:
                self.cursor.execute(query)

            return self.cursor
        except Exception as e:
            messagebox.showerror("Query Error", f"Error executing query: {e}")
            return None

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

        query = f"INSERT INTO {self.current_table} ({columns}) VALUES ({placeholders})"

        cursor = self.execute_query(query, values)
        if cursor:
            try:
                self.conn.commit()
                messagebox.showinfo("Success", "Record inserted successfully!")
                # Clear entries after successful insert
                for entry in self.entries.values():
                    entry.delete(0, tk.END)
            except Exception as e:
                self.conn.rollback()
                messagebox.showerror("Error", f"Error inserting record: {e}")
            finally:
                self.close_cursor()

    def create_cursor(self):
        """Create a new cursor if connection exists"""
        try:
            if self.conn:
                if self.cursor:
                    self.cursor.close()
                self.cursor = self.conn.cursor()
                return True
            return False
        except Exception as e:
            messagebox.showerror("Error", f"Failed to create cursor: {e}")
            return False

    def close_cursor(self):
        """Safely close the cursor"""
        try:
            if self.cursor:
                self.cursor.close()
                self.cursor = None
        except Exception as e:
            print(f"Error closing cursor: {e}")

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
        self.delete_tree = self.configure_treeview(delete_frame, columns)
        
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

if __name__ == "__main__":
    root = tk.Tk()
    app = HealthNetworkApp(root)
    root.mainloop()