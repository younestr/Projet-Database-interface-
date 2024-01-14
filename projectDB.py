import mysql.connector
from tkinter import Tk, Label, Listbox, Scrollbar, StringVar, filedialog, Entry, Button, OptionMenu, END, Y, RIGHT, LEFT, W, Toplevel, IntVar, Checkbutton, ttk, messagebox
import csv

# Replace with your actual database credentials
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'password',
    'database': 'projectDB'
}

def get_column_info(table_name):
    cursor.execute(f"DESCRIBE {table_name}")
    columns_info = cursor.fetchall()
    return columns_info

def get_table_list():
    cursor.execute("SHOW TABLES")
    tables = [table[0] for table in cursor.fetchall()]
    return tables


def update_table_dropdown():
    tables = get_table_list()
    selected_table.set(tables[0])  # Set the default selected table
    table_dropdown['menu'].delete(0, 'end')  # Clear existing menu items

    for table in tables:
        table_dropdown['menu'].add_command(label=table, command=lambda t=table: selected_table.set(t))

def export_data(selected_columns, rows):
    if not rows:
        messagebox.showinfo("Info", "No data to export.")
        return

    try:
        filename = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
        if filename:
            with open(filename, 'w', newline='') as csvfile:
                csv_writer = csv.writer(csvfile)
                
                # Write header
                header = [column[0] for column in selected_columns]
                csv_writer.writerow(header)
                
                # Write data
                csv_writer.writerows(rows)

            messagebox.showinfo("Info", "Data exported successfully.")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")

def proceed_to_fields(num_fields_entry, table_name_entry):
    num_fields_value = num_fields_entry.get()
    if not num_fields_value.isdigit():
        messagebox.showerror("Error", "Please enter a valid number for the fields.")
        return

    num_fields = int(num_fields_value)
    field_entries = []
    
    create_fields_window = Toplevel(root)
    create_fields_window.title("Create Fields")

    for i in range(num_fields):
        field_name_label = Label(create_fields_window, text=f"Field {i + 1} Name:")
        field_name_label.grid(row=i, column=0, padx=10, pady=5, sticky='W')
        field_name_entry = Entry(create_fields_window, width=30)
        field_name_entry.grid(row=i, column=1, padx=10, pady=5)

        # Dropdown menu for field types
        field_types = ["VARCHAR", "INT", "FLOAT", "DATETIME", "DATE"]
        field_type_label = Label(create_fields_window, text="Field Type:")
        field_type_label.grid(row=i, column=2, padx=10, pady=5, sticky='W')
        selected_field_type = StringVar(create_fields_window)
        selected_field_type.set(field_types[0])  # Set the default selected field type
        field_type_dropdown = OptionMenu(create_fields_window, selected_field_type, *field_types)
        field_type_dropdown.grid(row=i, column=3, padx=10, pady=5)

        field_entries.append((field_name_entry, selected_field_type))

    # Button to create the new table
    create_table_button = Button(create_fields_window, text="Create Table", command=lambda: execute_create_new_table(table_name_entry.get(), num_fields_entry.get(), field_entries, create_fields_window))
    create_table_button.grid(row=num_fields, column=0, columnspan=4, pady=10)

    
def create_new_table():
    global new_table_window  # Make new_table_window global
    new_table_window = Toplevel(root)
    new_table_window.title("Create New Table")

    # Entry for table name
    table_name_label = Label(new_table_window, text="Table Name:")
    table_name_label.grid(row=0, column=0, padx=10, pady=5, sticky='W')
    table_name_entry = Entry(new_table_window, width=30)
    table_name_entry.grid(row=0, column=1, padx=10, pady=5)

    # Entry for the number of fields
    num_fields_label = Label(new_table_window, text="Number of Fields:")
    num_fields_label.grid(row=1, column=0, padx=10, pady=5, sticky='W')
    num_fields_entry = Entry(new_table_window, width=10)
    num_fields_entry.grid(row=1, column=1, padx=10, pady=5)

    # Button to proceed to entering fields
    proceed_button = Button(new_table_window, text="Proceed", command=lambda: proceed_to_fields(num_fields_entry, table_name_entry))
    proceed_button.grid(row=2, column=0, columnspan=2, pady=10)

# Modify the execute_create_new_table function accordingly
def execute_create_new_table(table_name, num_fields, field_entries, create_fields_window):
    # Check if num_fields is a valid integer
    if not num_fields.isdigit():
        messagebox.showerror("Error", "Please enter a valid number for the fields.")
        return

    num_fields = int(num_fields)
    
    # Get the field names and types from the entries
    fields = [(entry[0].get(), entry[1].get()) for entry in field_entries]

    # Check if any field names are empty
    if any(not field[0] for field in fields):
        messagebox.showerror("Error", "Please enter names for all fields.")
        return

    # Create the SQL query for table creation
    query = f"CREATE TABLE {table_name} ({', '.join([f'{field[0]} {field[1]}' for field in fields])})"
    
    # Execute the query
    try:
        cursor.execute(query)
        conn.commit()

        # Notify the user about successful table creation
        messagebox.showinfo("Success", f"Table '{table_name}' created successfully!")
    except mysql.connector.Error as err:
        # Display error message if table creation fails
        messagebox.showerror("Error", f"Error: {err}")

    # Close the create fields window
    create_fields_window.destroy()



def execute_create_table_query(table_name):
    query = f"CREATE TABLE {table_name} (id INT PRIMARY KEY, name VARCHAR(255))"
    cursor.execute(query)
    conn.commit()

    # Notify the user about successful table creation
    result_listbox.delete(0, END)
    result_listbox.insert(END, f"Table '{table_name}' created successfully!")

    # Update the table dropdown menu
    update_table_dropdown()

def select_data():
    selected_table_value = selected_table.get()
    columns_info = get_column_info(selected_table_value)

    # Create a new window for field selection and conditions
    select_window = Toplevel(root)
    select_window.title(f"Select Fields from {selected_table_value}")

    # IntVars for each column
    selected_fields = {column[0]: IntVar() for column in columns_info}
    
    # Checkbuttons for each column
    for i, column_info in enumerate(columns_info):
        column_name = column_info[0]
        Checkbutton(select_window, text=column_name, variable=selected_fields[column_name]).grid(row=i, column=0, padx=10, pady=5, sticky=W)

    # Dropdown menu for conditions based on selected fields
    condition_label = Label(select_window, text="Conditions:")
    condition_label.grid(row=len(columns_info), column=0, padx=10, pady=5, sticky=W)
    conditions = ["=", ">", ">=", "<", "<=", "!=", "IS NULL", "IS NOT NULL", "LIKE", "NOT LIKE"]
    selected_conditions = {column[0]: StringVar() for column in columns_info}
    condition_dropdowns = {}
    
    for i, column_info in enumerate(columns_info):
        column_name = column_info[0]
        condition_dropdowns[column_name] = OptionMenu(select_window, selected_conditions[column_name], *conditions)
        condition_dropdowns[column_name].grid(row=i, column=1, padx=10, pady=5)

    # Entry widget for condition value
    condition_value_label = Label(select_window, text="Values:")
    condition_value_label.grid(row=len(columns_info) + 1, column=0, padx=10, pady=5, sticky=W)
    condition_value_entry = Entry(select_window, width=30)
    condition_value_entry.grid(row=len(columns_info) + 1, column=1, padx=10, pady=5)

    # Button to select data
    select_data_button = Button(select_window, text="Select Data", command=lambda: execute_select_query(selected_fields, selected_conditions, columns_info, selected_table_value, condition_value_entry.get()))
    select_data_button.grid(row=len(columns_info) + 2, column=0, columnspan=2, pady=10)

def execute_select_query(selected_fields, selected_conditions, columns_info, table_name, condition_value):
    selected_columns = [column_info[0] for column_info in columns_info if selected_fields[column_info[0]].get() == 1]

    # If no fields are selected, default to selecting all fields
    if not selected_columns:
        selected_columns = [column_info[0] for column_info in columns_info]

    conditions = []
    for column in selected_columns:
        selected_condition = selected_conditions[column].get()
        if selected_condition and condition_value:
            value = f"'{condition_value}'" if selected_condition not in ["IS NULL", "IS NOT NULL"] else ""
            conditions.append(f'{column} {selected_condition} {value}')

    where_clause = " AND ".join(conditions)
    query = f"SELECT {', '.join(selected_columns)} FROM {table_name}"
    if where_clause:
        query += f" WHERE {where_clause}"

    cursor.execute(query)
    rows = cursor.fetchall()

    result_listbox.delete(0, END)  # Clear previous results

    for row in rows:
        result_listbox.insert(END, row)

    # Create a new window to display the results in a table
    afficher_table(table_name, rows, columns_info)
    
    # Show the export button only when there are results
    if rows:
        export_data_button.config(command=lambda: export_data(selected_columns, rows))
        export_data_button.grid()  # Show the button
    else:
        export_data_button.grid_remove()  # Hide the button initially

def afficher_table(table_name, data, columns_info):
    fenetre_resultats = Toplevel(root)
    fenetre_resultats.title(f"Table: {table_name}")

    # Create a Treeview for displaying data as a table
    tree = ttk.Treeview(fenetre_resultats)
    tree["columns"] = tuple(range(len(columns_info)))
    tree.heading("#0", text="Index")
    tree.column("#0", width=50)

    for col, column_info in zip(tree["columns"], columns_info):
        tree.heading(col, text=column_info[0])
        tree.column(col, width=100)

    for index, row in enumerate(data):
        tree.insert("", index, values=row, text=index)

    tree.pack(expand=True, fill="both")

def insert_data():
    selected_table_value = selected_table.get()
    columns_info = get_column_info(selected_table_value)

    # Create a new window for data insertion
    insert_window = Toplevel(root)
    insert_window.title(f"Insert Data into {selected_table_value}")

    # Entry widgets for each column
    entry_values = {column[0]: Entry(insert_window, width=30) for column in columns_info}

    for i, (column_info, entry) in enumerate(zip(columns_info, entry_values.values())):
        column_name = column_info[0]
        Label(insert_window, text=f"{column_name}:").grid(row=i, column=0, padx=10, pady=5, sticky=W)
        entry.grid(row=i, column=1, padx=10, pady=5)

    # Button to insert data
    insert_data_button = Button(insert_window, text="Insert Data", command=lambda: execute_insert_query(selected_table_value, entry_values))
    insert_data_button.grid(row=len(columns_info), column=0, columnspan=2, pady=10)

def execute_insert_query(table_name, entry_values):
    columns = ', '.join(entry_values.keys())
    values = ', '.join(f"'{entry.get()}'" for entry in entry_values.values())
    query = f"INSERT INTO {table_name} ({columns}) VALUES ({values})"
    
    cursor.execute(query)
    conn.commit()

    # Notify the user about successful insertion
    result_listbox.delete(0, END)
    result_listbox.insert(END, "Data inserted successfully!")

    # Close the insert window
    insert_window.destroy()


def delete_data():
    selected_table_value = selected_table.get()
    columns_info = get_column_info(selected_table_value)

    # Create a new window for data deletion
    delete_window = Toplevel(root)
    delete_window.title(f"Delete Data from {selected_table_value}")

    # Radio buttons for choosing between deleting the whole table or specific rows
    delete_option = StringVar()
    delete_option.set("delete_table")  # Default option

    delete_table_radio = ttk.Radiobutton(delete_window, text="Delete Whole Table", variable=delete_option, value="delete_table")
    delete_table_radio.grid(row=0, column=0, padx=10, pady=5, sticky=W)

    delete_rows_radio = ttk.Radiobutton(delete_window, text="Delete Specific Rows", variable=delete_option, value="delete_rows")
    delete_rows_radio.grid(row=1, column=0, padx=10, pady=5, sticky=W)

    # Button to initiate deletion
    delete_button = Button(delete_window, text="Delete", command=lambda: execute_delete_query(selected_table_value, delete_option.get(), columns_info, delete_window))
    delete_button.grid(row=2, column=0, padx=10, pady=10)


def execute_delete_query(table_name, delete_option, columns_info, delete_window):
    if delete_option == "delete_table":
        # Display a warning message before deleting the whole table
        response = messagebox.askquestion("Warning", "Are you sure you want to delete the whole table?", icon='warning')
        if response == 'no':
            return  # User chose not to proceed with the deletion

        # Delete the whole table from the database
        query = f"DROP TABLE {table_name}"
    elif delete_option == "delete_rows":
        # Create a new window for selecting conditions
        condition_window = Toplevel(delete_window)
        condition_window.title(f"Select Conditions for Deleting Rows from {table_name}")

        # Dropdown menu for selecting the column for WHERE condition
        where_column_label = Label(condition_window, text="Select WHERE Column:")
        where_column_label.grid(row=0, column=0, padx=10, pady=5, sticky=W)

        where_columns = [column_info[0] for column_info in columns_info]
        selected_where_column = StringVar()
        selected_where_column.set(where_columns[0])  # Set the default selected column
        where_column_dropdown = OptionMenu(condition_window, selected_where_column, *where_columns)
        where_column_dropdown.grid(row=0, column=1, padx=10, pady=5)

        # Entry widget for WHERE condition value
        where_value_label = Label(condition_window, text="WHERE Value:")
        where_value_label.grid(row=1, column=0, padx=10, pady=5, sticky=W)

        where_value_entry = Entry(condition_window, width=30)
        where_value_entry.grid(row=1, column=1, padx=10, pady=5)

        # Dropdown menu for selecting the operator of comparison
        operator_label = Label(condition_window, text="Select Comparison Operator:")
        operator_label.grid(row=2, column=0, padx=10, pady=5, sticky=W)

        operators = ["=", ">", ">=", "<", "<=", "!=", "LIKE", "NOT LIKE"]
        selected_operator = StringVar()
        selected_operator.set(operators[0])  # Set the default selected operator
        operator_dropdown = OptionMenu(condition_window, selected_operator, *operators)
        operator_dropdown.grid(row=2, column=1, padx=10, pady=5)

        # Button to confirm deletion
        confirm_button = Button(condition_window, text="Delete Rows", command=lambda: execute_delete_rows_query(table_name, selected_where_column.get(), where_value_entry.get(), selected_operator.get(), condition_window))
        confirm_button.grid(row=3, column=0, columnspan=2, pady=10)

        return  # Skip executing the main delete query in this case

    # Execute the query
    cursor.execute(query)
    conn.commit()

    # Notify the user about successful deletion
    result_listbox.delete(0, END)
    result_listbox.insert(END, "Data deleted successfully!")

    # Close the delete window
    update_table_dropdown()
    delete_window.destroy()

def execute_delete_rows_query(table_name, where_column, where_value, operator, condition_window):
    # Construct the WHERE condition
    where_condition = f"{where_column} {operator} '{where_value}'"
    query = f"DELETE FROM {table_name} WHERE {where_condition}"

    # Execute the query
    cursor.execute(query)
    conn.commit()

    # Notify the user about successful deletion
    result_listbox.delete(0, END)
    result_listbox.insert(END, "Data deleted successfully!")

    # Close the condition window
    condition_window.destroy()




def update_data():
    selected_table_value = selected_table.get()
    columns_info = get_column_info(selected_table_value)

    # Create a new window for data update
    update_window = Toplevel(root)
    update_window.title(f"Update Data in {selected_table_value}")

    # Section 1: Selecting the WHERE condition
    where_frame = ttk.Frame(update_window)
    where_frame.grid(row=0, column=0, padx=10, pady=5)

    # Dropdown menu for selecting the column for WHERE condition
    where_column_label = Label(where_frame, text="Select WHERE Column:")
    where_column_label.grid(row=0, column=0, padx=10, pady=5, sticky=W)

    where_columns = [column_info[0] for column_info in columns_info]
    selected_where_column = StringVar()
    selected_where_column.set(where_columns[0])  # Set the default selected column
    where_column_dropdown = OptionMenu(where_frame, selected_where_column, *where_columns)
    where_column_dropdown.grid(row=0, column=1, padx=10, pady=5)

    # Entry widget for WHERE condition value
    where_value_label = Label(where_frame, text="WHERE Value:")
    where_value_label.grid(row=1, column=0, padx=10, pady=5, sticky=W)

    where_value_entry = Entry(where_frame, width=30)
    where_value_entry.grid(row=1, column=1, padx=10, pady=5)

    # Dropdown menu for selecting the operator of comparison
    operator_label = Label(where_frame, text="Select Comparison Operator:")
    operator_label.grid(row=2, column=0, padx=10, pady=5, sticky=W)

    operators = ["=", ">", ">=", "<", "<=", "!=", "LIKE", "NOT LIKE"]
    selected_operator = StringVar()
    selected_operator.set(operators[0])  # Set the default selected operator
    operator_dropdown = OptionMenu(where_frame, selected_operator, *operators)
    operator_dropdown.grid(row=2, column=1, padx=10, pady=5)

    # Section 2: Updating values
    update_frame = ttk.Frame(update_window)
    update_frame.grid(row=1, column=0, padx=10, pady=5)

    # Entry widgets for each column to update
    entry_values = {column[0]: Entry(update_frame, width=30) for column in columns_info}

    for i, (column_info, entry) in enumerate(zip(columns_info, entry_values.values())):
        column_name = column_info[0]
        Label(update_frame, text=f"{column_name}:").grid(row=i, column=0, padx=10, pady=5, sticky=W)
        entry.grid(row=i, column=1, padx=10, pady=5)

    # Button to update data
    update_data_button = Button(update_window, text="Update Data", command=lambda: execute_update_query(selected_table_value, selected_where_column.get(), where_value_entry.get(), selected_operator.get(), entry_values))
    update_data_button.grid(row=2, column=0, padx=10, pady=10)

def execute_update_query(table_name, where_column, where_value, operator, entry_values):
    set_clause = ', '.join([f"{column} = '{entry.get()}'" for column, entry in entry_values.items()])
    where_condition = f"{where_column} {operator} '{where_value}'"

    query = f"UPDATE {table_name} SET {set_clause} WHERE {where_condition}"

    cursor.execute(query)
    conn.commit()

    # Notify the user about successful update
    result_listbox.delete(0, END)
    result_listbox.insert(END, "Data updated successfully!")

    # Close the update window
    update_window.destroy()

# Connect to the MySQL server
conn = mysql.connector.connect(**db_config)
cursor = conn.cursor()

# GUI setup
root = Tk()
root.title("MySQL Database Interface")

# Entry widget for query input
query_entry = Entry(root, width=60)
query_entry.grid(row=0, column=0, padx=10, pady=10, columnspan=3)

# Dropdown menu for selecting tables
tables = get_table_list()
selected_table = StringVar(root)
selected_table.set(tables[0])  # Set the default selected table
table_dropdown = OptionMenu(root, selected_table, *tables)
table_dropdown.grid(row=0, column=3, padx=10, pady=10)

# Buttons for common SQL procedures
buttons_frame = ttk.Frame(root)
buttons_frame.grid(row=1, column=0, padx=10, pady=5, columnspan=4)

def create_button(text, command):
    return Button(buttons_frame, text=text, command=command)

# Example buttons
select_button = create_button("Select", select_data)
insert_button = create_button("Insert", insert_data)
update_button = create_button("Update", update_data)
delete_button = create_button("Delete", delete_data)
create_table_button = create_button("Create Table", create_new_table)

# Export button (initially hidden)
export_data_button = create_button("Export Data", export_data)
export_data_button.grid(row=0, column=5, padx=5, pady=5)
export_data_button.grid_remove()  # Hide the button initially

# Place buttons in the frame
buttons = [select_button, insert_button, update_button, delete_button,create_table_button]
for i, button in enumerate(buttons):
    button.grid(row=0, column=i, padx=5, pady=5)

# Label for results
result_label = Label(root, text="Results:")
result_label.grid(row=2, column=0, padx=10, pady=5, sticky=W)

# Listbox for displaying results
result_listbox = Listbox(root, width=80, height=15)
result_listbox.grid(row=3, column=0, padx=10, pady=5, columnspan=4)

# Scrollbar for the listbox
scrollbar = Scrollbar(root, command=result_listbox.yview)
scrollbar.grid(row=3, column=4, sticky="ns", pady=5)
result_listbox.config(yscrollcommand=scrollbar.set)


# Run the GUI
root.mainloop()

# Close the cursor and connection
cursor.close()
conn.close()