import psycopg2
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
import re
import json
from pathlib import Path

# Root Window
root = Tk()
root.title('Hello')
root.iconbitmap('media/database.ico')
root.geometry('800x600')
root.resizable(False, False)
root.focus_force()

# default button style
button_bg = '#f5f5f5'
button_act_bg = '#d6d6d6'
button_fg = '#181818'
button_act_fg = '#181818'

# Variables for using credentials in all connections
connection_user = ""
connection_password = ""
connection_host = ""
connection_port = ""
connection_database = ""

# JSON default Credentials and login info for checkboxes memorizing
credentials_default = {"user": "", "password": "", "host": "", "port": "", "database": ""}
remember_info_default = {"remember user": 0, "remember password": 0,
                         "remember host": 0, "remember port": 0, "remember database": 0}

# Login data for extraction and global usage (intended to be blanks by default and filled later)
credentials_extracted = {"user": "", "password": "", "host": "", "port": "", "database": ""}
remember_info_extracted = {"remember user": 0, "remember password": 0,
                           "remember host": 0, "remember port": 0, "remember database": 0}


# Initialization program checks if credential files do exist and creates a new "default" ones if no files were found
# After that, it extracts info from files into "extracted" variables
def initialization():
    # Function to create default credentials file
    def create_credentials():
        with open('login_credentials.json', 'w') as credentials_store_command:
            json.dump(credentials_default, credentials_store_command)

    # Function to create default "remember" file
    def create_remember_info():
        with open('login_remember.json', 'w') as remember_store_command:
            json.dump(remember_info_default, remember_store_command)

    # Path checks if files exist
    credentials_path = Path('login_credentials.json')
    print("Credentials file exists: " + str(credentials_path.is_file()))
    remember_info_path = Path('login_remember.json')
    print("Remember info file exists: " + str(remember_info_path.is_file()))

    # If no files found - a new ones created
    if not credentials_path.is_file():
        create_credentials()
        print("login_credentials.json created")
    else:
        pass
    # Same for second file
    if not remember_info_path.is_file():
        create_remember_info()
        print("login_remember.json created")
    else:
        pass

    # Read, insert into "extracted" and print Credentials JSON
    def read_credentials():
        global credentials_extracted
        with open('login_credentials.json', 'r') as login_extract_command:
            credentials_extracted = json.load(login_extract_command)
            print(credentials_extracted)
    read_credentials()

    # Read, insert into "extracted" and print Remember info JSON
    def read_remember_info():
        global remember_info_extracted
        with open('login_remember.json', 'r') as remember_extract_command:
            remember_info_extracted = json.load(remember_extract_command)
            print(remember_info_extracted)
    read_remember_info()


initialization()

# Putting login info into variables from extractions of .json file
user_login = str(credentials_extracted["user"])
password_login = str(credentials_extracted["password"])
host_login = str(credentials_extracted["host"])
port_login = str(credentials_extracted["port"])
database_login = str(credentials_extracted["database"])

# Variables for working with checkboxes, also extracted
variable_username = IntVar(value=int(remember_info_extracted["remember user"]))
variable_password = IntVar(value=int(remember_info_extracted["remember password"]))
variable_host = IntVar(value=int(remember_info_extracted["remember host"]))
variable_port = IntVar(value=int(remember_info_extracted["remember port"]))
variable_database = IntVar(value=int(remember_info_extracted["remember database"]))


# UI for login: Gets info from json into fields and checkboxes; Tries to log in and rewrite existing json files
def login_function():
    # Person Window
    login_window = Toplevel()
    login_window.title('Authorization')
    login_window.iconbitmap('media/database.ico')
    login_window.geometry('480x320')
    login_window.resizable(False, False)
    login_window.focus_force()

    # Opening management
    root.state('withdrawn')

    # Closing management
    def close_login():
        login_window.destroy()
        root.state('normal')
        root.focus_force()

    # Closing protocol
    login_window.protocol("WM_DELETE_WINDOW", close_login)

    # UI Text Elements
    header_label = Label(login_window, text='Login', font=("Courier", 12))
    header_label.grid(row=0, column=1, padx=25, pady=10)

    user_label = Label(login_window, text='User', font=("Courier", 10))
    user_label.grid(row=1, column=0, padx=25, pady=10)
    user_entry = Entry(login_window, font=("Courier", 10))
    user_entry.grid(row=1, column=1, padx=25, pady=10)

    password_label = Label(login_window, text='Password', font=("Courier", 10))
    password_label.grid(row=2, column=0, padx=25, pady=10)
    password_entry = Entry(login_window, font=("Courier", 10), show="*")
    password_entry.grid(row=2, column=1, padx=25, pady=10)

    host_label = Label(login_window, text='Host', font=("Courier", 10))
    host_label.grid(row=3, column=0, padx=25, pady=10)
    host_entry = Entry(login_window, font=("Courier", 10))
    host_entry.grid(row=3, column=1, padx=25, pady=10)

    port_label = Label(login_window, text='Port', font=("Courier", 10))
    port_label.grid(row=4, column=0, padx=25, pady=10)
    port_entry = Entry(login_window, font=("Courier", 10))
    port_entry.grid(row=4, column=1, padx=25, pady=10)

    database_label = Label(login_window, text='Database', font=("Courier", 10))
    database_label.grid(row=5, column=0, padx=25, pady=10)
    database_entry = Entry(login_window, font=("Courier", 10))
    database_entry.grid(row=5, column=1, padx=25, pady=10)

    # UI Buttons
    submit_button = Button(login_window, text="Submit", fg=button_fg, activeforeground=button_act_fg, bg=button_bg,
                           activebackground=button_act_bg, font=("Courier", 12),
                           command=lambda: submit_command(), borderwidth=1)
    submit_button.grid(row=6, column=1, padx=25, pady=10, sticky='WE')

    # UI checkboxes
    user_checkbox = ttk.Checkbutton(login_window, text="Remember User", variable=variable_username, onvalue=1,
                                    offvalue=0)
    user_checkbox.grid(row=1, column=3, sticky="W")

    password_checkbox = ttk.Checkbutton(login_window, text="Remember Password", variable=variable_password, onvalue=1,
                                        offvalue=0)
    password_checkbox.grid(row=2, column=3, sticky="W")

    host_checkbox = ttk.Checkbutton(login_window, text="Remember Host", variable=variable_host, onvalue=1, offvalue=0)
    host_checkbox.grid(row=3, column=3, sticky="W")

    port_checkbox = ttk.Checkbutton(login_window, text="Remember Port", variable=variable_port, onvalue=1, offvalue=0)
    port_checkbox.grid(row=4, column=3, sticky="W")

    database_checkbox = ttk.Checkbutton(login_window, text="Remember Database", variable=variable_database, onvalue=1,
                                        offvalue=0)
    database_checkbox.grid(row=5, column=3, sticky="W")

    # Tries to log in with extracted info and rewrite json files
    def submit_command():
        # Try to connect on click
        try:
            connection = psycopg2.connect(user=user_entry.get(),
                                          password=password_entry.get(),
                                          host=host_entry.get(),
                                          port=port_entry.get(),
                                          database=database_entry.get())
            cursor = connection.cursor()
            cursor.execute("SELECT version();")
            record = cursor.fetchone()
            # Connection info
            print("Connected to: ", record)
            print("Connection dsn parameters:")
            print(connection.get_dsn_parameters())

        except (Exception, psycopg2.Error) as error:
            print("Error while connecting to PostgreSQL: ", error)
            messagebox.showerror("Error", "Incorrect credentials")
        finally:
            # noinspection PyUnboundLocalVariable
            if connection:
                # noinspection PyUnboundLocalVariable
                cursor.close()
                # noinspection PyUnboundLocalVariable
                connection.close()
                print("PostgreSQL connection is closed.")

        # If code above is successful, sets pre-existing variables for usage in all connections
        global connection_user
        global connection_password
        global connection_host
        global connection_port
        global connection_database
        connection_user = user_entry.get()
        connection_password = password_entry.get()
        connection_host = host_entry.get()
        connection_port = port_entry.get()
        connection_database = database_entry.get()
        
        # Create variables to check with checkboxes in cases when they're checked or unchecked
        user_variable_prepare = ""
        if variable_username.get() == 1:
            user_variable_prepare = user_entry.get()
        else:
            pass
        password_variable_prepare = ""
        if variable_password.get() == 1:
            password_variable_prepare = password_entry.get()
        else:
            pass
        host_variable_prepare = ""
        if variable_host.get() == 1:
            host_variable_prepare = host_entry.get()
        else:
            pass
        port_variable_prepare = ""
        if variable_port.get() == 1:
            port_variable_prepare = port_entry.get()
        else:
            pass
        database_variable_prepare = ""
        if variable_database.get() == 1:
            database_variable_prepare = database_entry.get()
        else:
            pass
            
        # Acquire new login info for storing in files
        credentials_new = {"user": user_variable_prepare, "password": password_variable_prepare,
                           "host": host_variable_prepare, "port": port_variable_prepare,
                           "database": database_variable_prepare}
        remember_info_new = {"remember user": variable_username.get(), "remember password": variable_password.get(),
                             "remember host": variable_host.get(), "remember port": variable_port.get(),
                             "remember database": variable_database.get()}

        # Write new info into json files
        with open('login_credentials.json', 'w') as credentials_store_command:
            json.dump(credentials_new, credentials_store_command)
        with open('login_remember.json', 'w') as remember_store_command:
            json.dump(remember_info_new, remember_store_command)

        # Passing login screen
        messagebox.showinfo("Success", "Authorization successful, connection established.")
        close_login()

    # Post-creation fields filling
    user_entry.insert(0, user_login)
    password_entry.insert(0, password_login)
    host_entry.insert(0, host_login)
    port_entry.insert(0, port_login)
    database_entry.insert(0, database_login)


def choose_person():
    # Person Window
    person_window = Toplevel()
    person_window.title('Person')
    person_window.iconbitmap('media/database.ico')
    person_window.geometry('980x670')
    person_window.resizable(False, False)
    person_window.focus_force()

    # Opening management
    root.state('withdrawn')

    # Closing management
    def close_person():
        person_window.destroy()
        root.state('normal')
        root.focus_force()

    # Closing protocol
    person_window.protocol("WM_DELETE_WINDOW", close_person)

    # LEFT Person UI labels and entries
    person_label = Label(person_window, text='Person', font=("Courier", 12))
    person_label.grid(row=0, column=0, columnspan=2, padx=25, pady=10)

    person_id_label = Label(person_window, text='ID', font=("Courier", 10))
    person_id_label.grid(row=1, column=0, padx=10, pady=10)
    person_id_entry = Entry(person_window, font=("Courier", 10))
    person_id_entry.grid(row=1, column=1, padx=10, pady=10)

    person_firstname_label = Label(person_window, text='Firstname', font=("Courier", 10))
    person_firstname_label.grid(row=2, column=0, padx=10, pady=10)
    person_firstname_entry = Entry(person_window, font=("Courier", 10))
    person_firstname_entry.grid(row=2, column=1, padx=10, pady=10)

    person_lastname_label = Label(person_window, text='Lastname', font=("Courier", 10))
    person_lastname_label.grid(row=3, column=0, padx=10, pady=10)
    person_lastname_entry = Entry(person_window, font=("Courier", 10))
    person_lastname_entry.grid(row=3, column=1, padx=10, pady=10)

    person_patronym_label = Label(person_window, text='Patronym', font=("Courier", 10))
    person_patronym_label.grid(row=4, column=0, padx=10, pady=10)
    person_patronym_entry = Entry(person_window, font=("Courier", 10))
    person_patronym_entry.grid(row=4, column=1, padx=10, pady=10)

    person_dateofbirth_label = Label(person_window, text='Date of birth', font=("Courier", 10))
    person_dateofbirth_label.grid(row=5, column=0, padx=10, pady=10)

    # Date of birth validation
    def validate_date(date_input):
        check_result = re.match(r'^[\d]{4}[-][\d]{2}[-][\d]{2}$', date_input) is not None
        print(check_result)
        if check_result is False:
            person_dateofbirth_entry.delete(0, END)
            messagebox.showinfo('Attention!', "Please, either leave this field empty, or use format YY-MM-DD\n"
                                              "E.G. 2011-11-11")
        else:
            pass
        return check_result

    # .register is universal wrapper
    check_date_wrapper = (person_window.register(validate_date), '%P')
    # StringVar tracks value of Entry
    text_variable = StringVar()

    person_dateofbirth_entry = Entry(person_window, font=("Courier", 10),
                                     textvariable=text_variable,
                                     validate='focusout', validatecommand=check_date_wrapper)
    person_dateofbirth_entry.grid(row=5, column=1, padx=10, pady=10)

    person_city_label = Label(person_window, text='City', font=("Courier", 10))
    person_city_label.grid(row=6, column=0, padx=10, pady=10)
    person_city_entry = Entry(person_window, font=("Courier", 10))
    person_city_entry.grid(row=6, column=1, padx=10, pady=10)

    person_street_label = Label(person_window, text='Street', font=("Courier", 10))
    person_street_label.grid(row=7, column=0, padx=10, pady=10)
    person_street_entry = Entry(person_window, font=("Courier", 10))
    person_street_entry.grid(row=7, column=1, padx=10, pady=10)

    person_building_label = Label(person_window, text='Building', font=("Courier", 10))
    person_building_label.grid(row=8, column=0, padx=10, pady=10)
    person_building_entry = Entry(person_window, font=("Courier", 10))
    person_building_entry.grid(row=8, column=1, padx=10, pady=10)

    person_apartment_label = Label(person_window, text='Apartment', font=("Courier", 10))
    person_apartment_label.grid(row=9, column=0, padx=10, pady=10)
    person_apartment_entry = Entry(person_window, font=("Courier", 10))
    person_apartment_entry.grid(row=9, column=1, padx=10, pady=10)

    # LEFT Person UI buttons
    person_clear_button = Button(person_window, text="Clear Fields", fg=button_fg, activeforeground=button_act_fg,
                                 bg='#ffcc02', activebackground='#e6b802', font=("Courier", 10), borderwidth=1)
    person_clear_button.grid(row=10, column=0, columnspan=2, padx=10, pady=10, sticky='we')

    person_search_button = Button(person_window, text="Search", fg=button_fg, activeforeground=button_act_fg,
                                  bg=button_bg, activebackground=button_act_bg, font=("Courier", 10), borderwidth=1)
    person_search_button.grid(row=11, column=0, columnspan=2, padx=10, pady=10, sticky='we')

    person_edit_button = Button(person_window, text="Edit", fg=button_fg, activeforeground=button_act_fg,
                                bg='#6677cc', activebackground='#546099', font=("Courier", 10), borderwidth=1)
    person_edit_button.grid(row=12, column=0, columnspan=2, padx=10, pady=10, sticky='we')

    person_create_button = Button(person_window, text="Create New", fg=button_fg, activeforeground=button_act_fg,
                                  bg='#66cc77', activebackground='#549960', font=("Courier", 10), borderwidth=1)
    person_create_button.grid(row=13, column=0, columnspan=2, padx=10, pady=10, sticky='we')

    person_delete_button = Button(person_window, text="Delete", fg=button_fg, activeforeground=button_act_fg,
                                  bg='#c85a50', activebackground='#ae4137', font=("Courier", 10), borderwidth=1)
    person_delete_button.grid(row=14, column=0, columnspan=2, padx=10, pady=10, sticky='we')

    # RIGHT People UI label
    people_label = Label(person_window, text='People', font=("Courier", 12))
    people_label.grid(row=0, column=2, columnspan=2, padx=25, pady=10)

    # RIGHT list of people
    # RIGHT Frame base
    person_frame = Frame(person_window, bg='#6b6b6b', width=600)
    person_frame.grid(row=1, column=2, rowspan=12, padx=10, pady=10, sticky='nsew')
    # RIGHT Canvas
    person_canvas = Canvas(person_frame, bg='#f0f0f0', width=600)
    person_canvas.pack(side=LEFT, fill=BOTH, padx=2, pady=2)

    # RIGHT Scrollbar
    person_scrollbar = ttk.Scrollbar(person_window, orient=VERTICAL, command=person_canvas.yview)
    person_scrollbar.grid(row=1, column=3, rowspan=12, sticky='nsew')
    # RIGHT Configure Scrollbar
    # ! bind scrollbar "Y scroll" command to canvas
    person_canvas.configure(yscrollcommand=person_scrollbar.set)
    # ! ! restrict scroll region
    person_canvas.bind('<Configure>', lambda e: person_canvas.configure(scrollregion=person_canvas.bbox('all')))

    # RIGHT Create content frame(window)
    content_frame = Frame(person_canvas, bg='#f0f0f0')
    person_canvas.create_window((2, 2), window=content_frame, anchor="nw", width=600)
    content_frame.grid_columnconfigure(0, weight=1)

    # Commands for buttons
    def person_clear():
        person_id_entry.delete(0, END)
        person_firstname_entry.delete(0, END)
        person_lastname_entry.delete(0, END)
        person_patronym_entry.delete(0, END)
        person_dateofbirth_entry.delete(0, END)
        person_city_entry.delete(0, END)
        person_street_entry.delete(0, END)
        person_building_entry.delete(0, END)
        person_apartment_entry.delete(0, END)

    def person_search():
        try:
            connection = psycopg2.connect(user=connection_user,
                                          password=connection_password,
                                          host=connection_host,
                                          port=connection_port,
                                          database=connection_database)
            cursor = connection.cursor()
            print("Connected to PostgreSQL;")

            # Getting column values from entries
            if person_id_entry.get():
                query_id = person_id_entry.get()
            else:
                query_id = None

            if person_firstname_entry.get():
                query_firstname = person_firstname_entry.get()
            else:
                query_firstname = None

            if person_lastname_entry.get():
                query_lastname = person_lastname_entry.get()
            else:
                query_lastname = None

            if person_patronym_entry.get():
                query_patronym = person_patronym_entry.get()
            else:
                query_patronym = None

            if person_dateofbirth_entry.get():
                query_dateofbirth = person_dateofbirth_entry.get()
            else:
                query_dateofbirth = None

            if person_city_entry.get():
                query_city = person_city_entry.get()
            else:
                query_city = None

            if person_street_entry.get():
                query_street = person_street_entry.get()
            else:
                query_street = None

            if person_building_entry.get():
                query_building = person_building_entry.get()
            else:
                query_building = None

            if person_apartment_entry.get():
                query_apartment = person_apartment_entry.get()
            else:
                query_apartment = None

            # PostgreSQL command
            query = """
                        SELECT * FROM person INNER JOIN address on person.addressid = address.id
                        WHERE (person.ID = %(ID)s OR %(ID)s IS NULL)
                        AND (firstname = %(firstname)s OR %(firstname)s IS NULL)
                        AND (lastname = %(lastname)s OR %(lastname)s IS NULL)
                        AND (patronym = %(patronym)s OR %(patronym)s IS NULL)
                        AND (dateofbirth = %(dateofbirth)s OR %(dateofbirth)s IS NULL)
                        AND (city = %(city)s OR %(city)s IS NULL)
                        AND (street = %(street)s OR %(street)s IS NULL)
                        AND (building = %(building)s OR %(building)s IS NULL)
                        AND (apartment = %(apartment)s OR %(apartment)s IS NULL)
                    """
            parameters = dict(ID=query_id, firstname=query_firstname, lastname=query_lastname, patronym=query_patronym,
                              dateofbirth=query_dateofbirth, city=query_city, street=query_street,
                              building=query_building, apartment=query_apartment)
            cursor.execute(query, parameters)

            print("Executing PostgreSQL query")
            result = cursor.fetchall()
            print("Result:", result)

            # Destroying(!) previous result
            for widget in content_frame.winfo_children():
                widget.destroy()
            # Checking if patronym exists
            for index, element in enumerate(result):
                def patronym_check():
                    patronym_element = element[3]
                    if patronym_element is None:
                        patronym_element = ""
                        return patronym_element
                    else:
                        return " " + patronym_element
                patronym_check_result = patronym_check()

                # Placing result in window as rows of buttons
                Button(
                    content_frame, text=f'{element[0]}. {element[1]} {element[2]}{patronym_check_result}, '
                                        f'{element[4]}, {element[7]}, {element[8]} {element[9]}, ap. {element[10]}',
                                        anchor="w",
                    command=lambda lamb_id=element[0], lamb_firstname=element[1], lamb_lastname=element[2],
                    lamb_patronym=patronym_check_result, lamb_dateofbirth=element[4], lamb_city=element[7],
                    lamb_street=element[8], lamb_building=element[9], lamb_apartment=element[10]:
                    [
                        person_id_entry.delete(0, END), person_id_entry.insert(0, lamb_id),
                        person_firstname_entry.delete(0, END), person_firstname_entry.insert(0, lamb_firstname),
                        person_lastname_entry.delete(0, END), person_lastname_entry.insert(0, lamb_lastname),
                        person_patronym_entry.delete(0, END), person_patronym_entry.insert(0, lamb_patronym.strip()),
                        person_dateofbirth_entry.delete(0, END), person_dateofbirth_entry.insert(0, lamb_dateofbirth),
                        person_city_entry.delete(0, END), person_city_entry.insert(0, lamb_city),
                        person_street_entry.delete(0, END), person_street_entry.insert(0, lamb_street),
                        person_building_entry.delete(0, END), person_building_entry.insert(0, lamb_building),
                        person_apartment_entry.delete(0, END), person_apartment_entry.insert(0, lamb_apartment)
                    ],
                    bg="#FFFFFF",
                    activebackground=button_bg,
                    borderwidth=1
                    ).grid(row=index, column=0, sticky='nsew', padx=1, pady=1)

        except (Exception, psycopg2.Error) as error:
            print("Error while connecting to PostgreSQL: ", error)
        finally:
            # noinspection PyUnboundLocalVariable
            if connection:
                # noinspection PyUnboundLocalVariable
                cursor.close()
                # noinspection PyUnboundLocalVariable
                connection.close()
                print("PostgreSQL connection is closed.")

    def person_edit():
        # Get ID from person window
        if person_id_entry.get():
            get_person_id = person_id_entry.get()
        else:
            messagebox.showerror("Warning!", "No ID is present!")
            return

        # Check if ID is valid
        try:
            id_management_connection = psycopg2.connect(user=connection_user,
                                                        password=connection_password,
                                                        host=connection_host,
                                                        port=connection_port,
                                                        database=connection_database)
            id_management_cursor = id_management_connection.cursor()
            print("Connected to PostgreSQL;")

            # Postgres command
            id_management_query = """
                            SELECT * FROM person WHERE ID = %(ID)s
                                  """
            id_management_parameters = dict(ID=get_person_id)
            id_management_cursor.execute(id_management_query, id_management_parameters)
            id_management_value = id_management_cursor.fetchall()
            print(id_management_value)
            if id_management_value:
                pass
            else:
                messagebox.showerror("Error!", "The ID is invalid!")
                return

        except (Exception, psycopg2.Error) as id_management_error:
            print("Error while connecting to PostgreSQL(ID validation): ", id_management_error)
            messagebox.showerror("Error!", "UNKNOWN ERROR")
        finally:
            # noinspection PyUnboundLocalVariable
            if id_management_connection:
                # noinspection PyUnboundLocalVariable
                id_management_cursor.close()
                # noinspection PyUnboundLocalVariable
                id_management_connection.close()
                print("PostgreSQL connection is closed.")

        # Person Window
        person_edit_window = Toplevel()
        person_edit_window.title('Edit')
        person_edit_window.iconbitmap('media/database.ico')
        person_edit_window.geometry('1020x830')
        person_edit_window.resizable(False, False)
        person_edit_window.focus_force()

        # Opening management
        person_window.state('withdrawn')

        # Closing management
        def close_person_edit():
            person_edit_window.destroy()
            person_window.state('normal')
            person_window.focus_force()

        # Closing protocol
        person_edit_window.protocol("WM_DELETE_WINDOW", close_person_edit)

        # UI LEFT UPPER
        edit_upper_frame = LabelFrame(person_edit_window, text="Edit", padx=10, pady=10)
        edit_upper_frame.grid(row=1, column=0, padx=10, pady=10)

        edit_person_label = Label(edit_upper_frame, text='Person', font=("Courier", 12))
        edit_person_label.grid(row=0, column=0, columnspan=2, padx=0, pady=0)

        edit_person_id_label = Label(edit_upper_frame, text='ID', font=("Courier", 10))
        edit_person_id_label.grid(row=1, column=0, padx=10, pady=10)
        edit_person_id_value = Label(edit_upper_frame, text=get_person_id, font=("Courier", 10),
                                     anchor='w', background='#f0f0f0', borderwidth=1, relief='sunken')
        edit_person_id_value.grid(row=1, column=1, padx=10, pady=10, sticky='we')

        edit_firstname_label = Label(edit_upper_frame, text='Firstname', font=("Courier", 10))
        edit_firstname_label.grid(row=2, column=0, padx=10, pady=10)
        edit_firstname_entry = Entry(edit_upper_frame, font=("Courier", 10))
        edit_firstname_entry.grid(row=2, column=1, padx=10, pady=10)

        edit_lastname_label = Label(edit_upper_frame, text='Lastname', font=("Courier", 10))
        edit_lastname_label.grid(row=3, column=0, padx=10, pady=10)
        edit_lastname_entry = Entry(edit_upper_frame, font=("Courier", 10))
        edit_lastname_entry.grid(row=3, column=1, padx=10, pady=10)

        edit_patronym_label = Label(edit_upper_frame, text='Patronym', font=("Courier", 10))
        edit_patronym_label.grid(row=4, column=0, padx=10, pady=10)
        edit_patronym_entry = Entry(edit_upper_frame, font=("Courier", 10))
        edit_patronym_entry.grid(row=4, column=1, padx=10, pady=10)

        edit_dateofbirth_label = Label(edit_upper_frame, text='Date of birth', font=("Courier", 10))
        edit_dateofbirth_label.grid(row=5, column=0, padx=10, pady=10)

        # Date of birth validation
        def edit_validate_date(date_input):
            check_result = re.match(r'^[\d]{4}[-][\d]{2}[-][\d]{2}$', date_input) is not None
            print(check_result)
            if check_result is False:
                edit_dateofbirth_entry.delete(0, END)
                messagebox.showinfo('Attention!', "Please, use format YY-MM-DD\n"
                                                  "E.G. 2011-11-11")
            else:
                pass
            return check_result

        # .register is universal wrapper
        edit_check_date_wrapper = (edit_upper_frame.register(edit_validate_date), '%P')
        # StringVar tracks value of Entry
        edit_text_variable = StringVar()

        edit_dateofbirth_entry = Entry(edit_upper_frame, font=("Courier", 10),
                                       textvariable=edit_text_variable,
                                       validate='focusout', validatecommand=edit_check_date_wrapper)
        edit_dateofbirth_entry.grid(row=5, column=1, padx=10, pady=10)

        # UI LEFT LOWER
        edit_lower_frame = LabelFrame(person_edit_window, text="Filter", padx=10, pady=10)
        edit_lower_frame.grid(row=2, column=0, padx=10, pady=10, sticky='we')

        edit_address_label = Label(edit_lower_frame, text='Address', font=("Courier", 12))
        edit_address_label.grid(row=0, column=0, columnspan=2, padx=0, pady=0)

        edit_address_id_label = Label(edit_lower_frame, text='ID', font=("Courier", 10))
        edit_address_id_label.grid(row=1, column=0, padx=10, pady=10)
        edit_address_id_value = Label(edit_lower_frame, text="", font=("Courier", 10),
                                      anchor='w', background='#f0f0f0', borderwidth=1, relief='sunken', width=24)
        edit_address_id_value.grid(row=1, column=1, padx=10, pady=10)

        edit_city_label = Label(edit_lower_frame, text='City', font=("Courier", 10))
        edit_city_label.grid(row=2, column=0, padx=10, pady=10)
        edit_city_entry = Entry(edit_lower_frame, font=("Courier", 10))
        edit_city_entry.grid(row=2, column=1, padx=10, pady=10, sticky='we')

        edit_street_label = Label(edit_lower_frame, text='Street', font=("Courier", 10))
        edit_street_label.grid(row=3, column=0, padx=10, pady=10)
        edit_street_entry = Entry(edit_lower_frame, font=("Courier", 10))
        edit_street_entry.grid(row=3, column=1, padx=10, pady=10, sticky='we')

        edit_building_label = Label(edit_lower_frame, text='Building', font=("Courier", 10))
        edit_building_label.grid(row=4, column=0, padx=10, pady=10)
        edit_building_entry = Entry(edit_lower_frame, font=("Courier", 10))
        edit_building_entry.grid(row=4, column=1, padx=10, pady=10, sticky='we')

        edit_apartment_label = Label(edit_lower_frame, text='Apartment', font=("Courier", 10))
        edit_apartment_label.grid(row=5, column=0, padx=10, pady=10)
        edit_apartment_entry = Entry(edit_lower_frame, font=("Courier", 10))
        edit_apartment_entry.grid(row=5, column=1, padx=10, pady=10, sticky='we')

        # UI LEFT create Buttons
        edit_upper_clear = Button(edit_upper_frame, text="Clear Fields", fg=button_fg,
                                  activeforeground=button_act_fg,
                                  bg='#ffcc02', activebackground='#e6b802', font=("Courier", 10), borderwidth=1)
        edit_upper_clear.grid(row=6, column=0, columnspan=2, padx=10, pady=10, sticky='we')

        edit_address_search = Button(edit_lower_frame, text="Search", fg=button_fg, activeforeground=button_act_fg,
                                     bg=button_bg, activebackground=button_act_bg, font=("Courier", 10), borderwidth=1)
        edit_address_search.grid(row=7, column=0, columnspan=2, padx=10, pady=10, sticky='we')

        edit_lower_clear = Button(edit_lower_frame, text="Clear Fields", fg=button_fg,
                                  activeforeground=button_act_fg,
                                  bg='#ffcc02', activebackground='#e6b802', font=("Courier", 10), borderwidth=1)
        edit_lower_clear.grid(row=6, column=0, columnspan=2, padx=10, pady=10, sticky='we')

        edit_edit_record = Button(person_edit_window, text="Update Record", fg=button_fg,
                                  activeforeground=button_act_fg, bg='#6677cc',
                                  activebackground='#546099', font=("Courier", 10), borderwidth=1)
        edit_edit_record.grid(row=3, column=0, columnspan=2, padx=10, pady=10, sticky='we')

        # UI RIGHT Address label
        edit_address_label = Label(person_edit_window, text='Address', font=("Courier", 12))
        edit_address_label.grid(row=0, column=2, columnspan=2, padx=25, pady=10)

        # RIGHT Address list
        # RIGHT Frame base
        edit_frame = Frame(person_edit_window, bg='#546099', width=600)
        edit_frame.grid(row=1, column=2, rowspan=2, padx=10, pady=10, sticky='nsew')
        # RIGHT Canvas
        edit_canvas = Canvas(edit_frame, bg='#f0f0f0', width=600)
        edit_canvas.pack(side=LEFT, fill=BOTH, padx=2, pady=2)

        # RIGHT Scrollbar
        edit_scrollbar = ttk.Scrollbar(person_edit_window, orient=VERTICAL, command=edit_canvas.yview)
        edit_scrollbar.grid(row=1, column=3, rowspan=2, sticky='nsew')
        # RIGHT Configure Scrollbar
        # * bind scrollbar "Y scroll" command to canvas
        edit_canvas.configure(yscrollcommand=edit_scrollbar.set)
        # * * restrict scroll region
        edit_canvas.bind('<Configure>', lambda e: edit_canvas.configure(scrollregion=edit_canvas.bbox('all')))

        # RIGHT Create content frame(window)
        edit_content_frame = Frame(edit_canvas, bg='#f0f0f0')
        edit_canvas.create_window((2, 2), window=edit_content_frame, anchor="nw", width=600)
        edit_content_frame.grid_columnconfigure(0, weight=1)

        # Def Commands
        def upper_clear():
            edit_firstname_entry.delete(0, END)
            edit_lastname_entry.delete(0, END)
            edit_patronym_entry.delete(0, END)
            edit_dateofbirth_entry.delete(0, END)

        def lower_clear():
            edit_address_id_value.config(text="")
            edit_city_entry.delete(0, END)
            edit_street_entry.delete(0, END)
            edit_building_entry.delete(0, END)
            edit_apartment_entry.delete(0, END)

        def edit_search_addresses():
            try:
                connection = psycopg2.connect(user=connection_user,
                                              password=connection_password,
                                              host=connection_host,
                                              port=connection_port,
                                              database=connection_database)
                cursor = connection.cursor()
                print("Connected to PostgreSQL;")

                # Getting values from addresses fields
                if edit_address_id_value.cget("text"):
                    edit_query_id = edit_address_id_value.cget("text")
                else:
                    edit_query_id = None

                if edit_city_entry.get():
                    edit_city_id = edit_city_entry.get()
                else:
                    edit_city_id = None

                if edit_street_entry.get():
                    edit_street_id = edit_street_entry.get()
                else:
                    edit_street_id = None

                if edit_building_entry.get():
                    edit_building_id = edit_building_entry.get()
                else:
                    edit_building_id = None

                if edit_apartment_entry.get():
                    edit_apartment_id = edit_apartment_entry.get()
                else:
                    edit_apartment_id = None

                # PostgreSQL command
                query = """
                            SELECT * FROM address
                            WHERE (city = %(city)s OR %(city)s IS NULL)
                            AND (street = %(street)s OR %(street)s IS NULL)
                            AND (building = %(building)s OR %(building)s IS NULL)
                            AND (apartment = %(apartment)s OR %(apartment)s IS NULL)
                        """
                # Legacy code chunk
                # SELECT * FROM address
                # WHERE (ID = %(ID)s OR %(ID)s IS NULL)
                # AND (city = %(city)s OR %(city)s IS NULL)
                # AND (street = %(street)s OR %(street)s IS NULL)
                # AND (building = %(building)s OR %(building)s IS NULL)
                # AND (apartment = %(apartment)s OR %(apartment)s IS NULL)

                parameters = dict(ID=edit_query_id, city=edit_city_id, street=edit_street_id,
                                  building=edit_building_id, apartment=edit_apartment_id)
                cursor.execute(query, parameters)
                print("Executing PostgreSQL query")

                # Fetch info into result
                result = cursor.fetchall()
                print("Result:", result)

                # Destroying(!) previous result
                for widget in edit_content_frame.winfo_children():
                    widget.destroy()
                # Placing result in window as rows of buttons
                for index, element in enumerate(result):
                    Button(
                        edit_content_frame, text=f'{element[0]}, {element[1]}, {element[2]}, {element[3]},'
                                                 f' ap. {element[4]}', anchor="w",
                        command=lambda lamb_id=element[0], lamb_city=element[1], lamb_street=element[2],
                        lamb_building=element[3], lamb_apartment=element[4]:
                        [
                            edit_address_id_value.config(text=""), edit_address_id_value.config(text=f"{lamb_id}"),
                            edit_city_entry.delete(0, END), edit_city_entry.insert(0, lamb_city),
                            edit_street_entry.delete(0, END), edit_street_entry.insert(0, lamb_street),
                            edit_building_entry.delete(0, END), edit_building_entry.insert(0, lamb_building),
                            edit_apartment_entry.delete(0, END), edit_apartment_entry.insert(0, lamb_apartment)
                        ],
                        bg="#FFFFFF",
                        activebackground=button_bg,
                        borderwidth=1
                        ).grid(row=index, column=0, sticky='nsew', padx=1, pady=1)

            except (Exception, psycopg2.Error) as search_error:
                print("Error while connecting to PostgreSQL: ", search_error)
            finally:
                # noinspection PyUnboundLocalVariable
                if connection:
                    # noinspection PyUnboundLocalVariable
                    cursor.close()
                    # noinspection PyUnboundLocalVariable
                    connection.close()
                    print("PostgreSQL connection is closed.")

        def edit_update_person():
            try:
                connection = psycopg2.connect(user=connection_user,
                                              password=connection_password,
                                              host=connection_host,
                                              port=connection_port,
                                              database=connection_database)
                cursor = connection.cursor()
                print("Connected to PostgreSQL;")

                # Check if person entries are filled
                if edit_person_id_value.cget("text"):
                    update_id_query = edit_person_id_value.cget("text")
                else:
                    messagebox.showerror("Warning!", "No valid ID is present!")
                    return

                if edit_firstname_entry.get():
                    update_firstname_query = edit_firstname_entry.get()
                else:
                    messagebox.showerror("Error", "Please, enter correct firstname")
                    return

                if edit_lastname_entry.get():
                    update_lastname_query = edit_lastname_entry.get()
                else:
                    messagebox.showerror("Error", "Please, enter correct lastname")
                    return

                if edit_patronym_entry.get():
                    update_patronym_query = edit_patronym_entry.get()
                else:
                    update_patronym_query = None

                if edit_dateofbirth_entry.get():
                    update_dateofbirth_query = edit_dateofbirth_entry.get()
                else:
                    messagebox.showerror("Error", "Please, enter correct date of birth")
                    return

                # Check if Address is present
                if edit_address_id_value.cget("text"):
                    update_addressid_query = edit_address_id_value.cget("text")
                else:
                    messagebox.showerror("Error", "Please, choose address id")
                    return

                # Confirm update
                ask = messagebox.askyesno("Confirm", "Apply Changes?")
                if ask:
                    pass
                else:
                    return

                # PostgreSQL command
                query = """
                            UPDATE person SET
                            firstname = %(firstname)s, lastname = %(lastname)s, patronym = %(patronym)s,
                            dateofbirth = %(dateofbirth)s, addressid = %(addressid)s
                            WHERE ID = %(ID)s
                        """
                parameters = dict(firstname=update_firstname_query, lastname=update_lastname_query,
                                  patronym=update_patronym_query, dateofbirth=update_dateofbirth_query,
                                  addressid=update_addressid_query, ID=update_id_query)
                cursor.execute(query, parameters)
                connection.commit()

            except (Exception, psycopg2.Error) as updating_error:
                print("Error while connecting to PostgreSQL: ", updating_error)
            finally:
                # noinspection PyUnboundLocalVariable
                if connection:
                    # noinspection PyUnboundLocalVariable
                    cursor.close()
                    # noinspection PyUnboundLocalVariable
                    connection.close()
                    print("PostgreSQL connection is closed.")

        # Add commands to buttons
        edit_upper_clear.configure(command=lambda: upper_clear())
        edit_lower_clear.configure(command=lambda: lower_clear())
        edit_address_search.configure(command=lambda: edit_search_addresses())
        edit_edit_record.configure(command=lambda: edit_update_person())

        # Insert data according to valid ID (Post-window-creation fields filling)
        try:
            id_management_connection = psycopg2.connect(user=connection_user,
                                                        password=connection_password,
                                                        host=connection_host,
                                                        port=connection_port,
                                                        database=connection_database)
            id_management_cursor = id_management_connection.cursor()
            print("Connected to PostgreSQL;")

            # PostgreSQL command to eject data
            id_management_query = """
                                    SELECT * FROM person INNER JOIN address on person.addressid = address.id
                                    WHERE person.ID = %(ID)s
                                  """
            id_management_parameters = dict(ID=get_person_id)
            id_management_cursor.execute(id_management_query, id_management_parameters)
            id_management_result = id_management_cursor.fetchone()

            # Empty Patronym workaround
            if id_management_result[3] is None:
                tuple_convertor = list(id_management_result)
                tuple_convertor[3] = ""
                id_management_result = tuple(tuple_convertor)
            else:
                pass

            # Insert person info into entries
            edit_firstname_entry.insert(0, id_management_result[1])
            edit_lastname_entry.insert(0, id_management_result[2])
            edit_patronym_entry.insert(0, id_management_result[3])
            edit_dateofbirth_entry.insert(0, id_management_result[4])
            edit_address_id_value.config(text=f"{id_management_result[6]}")
            edit_city_entry.insert(0, id_management_result[7])
            edit_street_entry.insert(0, id_management_result[8])
            edit_building_entry.insert(0, id_management_result[9])
            edit_apartment_entry.insert(0, id_management_result[10])

        except (Exception, psycopg2.Error) as error:
            print("Error while connecting to PostgreSQL(Data filling): ", error)
        finally:
            # noinspection PyUnboundLocalVariable
            if id_management_connection:
                # noinspection PyUnboundLocalVariable
                id_management_cursor.close()
                # noinspection PyUnboundLocalVariable
                id_management_connection.close()
                print("PostgreSQL connection is closed.")

    def person_create():
        # Person Window
        person_create_window = Toplevel()
        person_create_window.title('Create')
        person_create_window.iconbitmap('media/database.ico')
        person_create_window.geometry('1020x788')
        person_create_window.resizable(False, False)
        person_create_window.focus_force()

        # Opening management
        person_window.state('withdrawn')

        # Closing management
        def close_person_create():
            person_create_window.destroy()
            person_window.state('normal')
            person_window.focus_force()

        # Closing protocol
        person_create_window.protocol("WM_DELETE_WINDOW", close_person_create)

        # UI LEFT UPPER
        create_upper_frame = LabelFrame(person_create_window, text="Insert", padx=10, pady=10)
        create_upper_frame.grid(row=1, column=0, padx=10, pady=10)

        create_person_label = Label(create_upper_frame, text='Person', font=("Courier", 12))
        create_person_label.grid(row=0, column=0, columnspan=2, padx=0, pady=0)

        create_firstname_label = Label(create_upper_frame, text='Firstname', font=("Courier", 10))
        create_firstname_label.grid(row=1, column=0, padx=10, pady=10)
        create_firstname_entry = Entry(create_upper_frame, font=("Courier", 10))
        create_firstname_entry.grid(row=1, column=1, padx=10, pady=10)

        create_lastname_label = Label(create_upper_frame, text='Lastname', font=("Courier", 10))
        create_lastname_label.grid(row=2, column=0, padx=10, pady=10)
        create_lastname_entry = Entry(create_upper_frame, font=("Courier", 10))
        create_lastname_entry.grid(row=2, column=1, padx=10, pady=10)

        create_patronym_label = Label(create_upper_frame, text='Patronym', font=("Courier", 10))
        create_patronym_label.grid(row=3, column=0, padx=10, pady=10)
        create_patronym_entry = Entry(create_upper_frame, font=("Courier", 10))
        create_patronym_entry.grid(row=3, column=1, padx=10, pady=10)

        create_dateofbirth_label = Label(create_upper_frame, text='Date of birth', font=("Courier", 10))
        create_dateofbirth_label.grid(row=4, column=0, padx=10, pady=10)

        # Date of birth validation
        def create_validate_date(date_input):
            check_result = re.match(r'^[\d]{4}[-][\d]{2}[-][\d]{2}$', date_input) is not None
            print(check_result)
            if check_result is False:
                create_dateofbirth_entry.delete(0, END)
                messagebox.showinfo('Attention!', "Please, use format YY-MM-DD\n"
                                                  "E.G. 2011-11-11")
            else:
                pass
            return check_result

        # .register is universal wrapper
        create_check_date_wrapper = (create_upper_frame.register(create_validate_date), '%P')
        # StringVar tracks value of Entry
        create_text_variable = StringVar()

        create_dateofbirth_entry = Entry(create_upper_frame, font=("Courier", 10),
                                         textvariable=create_text_variable,
                                         validate='focusout', validatecommand=create_check_date_wrapper)
        create_dateofbirth_entry.grid(row=4, column=1, padx=10, pady=10)

        # UI LEFT LOWER
        create_lower_frame = LabelFrame(person_create_window, text="Filter", padx=10, pady=10)
        create_lower_frame.grid(row=2, column=0, padx=10, pady=10, sticky='we')

        create_address_label = Label(create_lower_frame, text='Address', font=("Courier", 12))
        create_address_label.grid(row=0, column=0, columnspan=2, padx=0, pady=0)

        create_id_label = Label(create_lower_frame, text='ID', font=("Courier", 10))
        create_id_label.grid(row=1, column=0, padx=10, pady=10)
        create_id_value = Label(create_lower_frame, text="", font=("Courier", 10),
                                anchor='w', background='#f0f0f0', borderwidth=1, relief='sunken', width=24)
        create_id_value.grid(row=1, column=1, padx=10, pady=10, sticky='we')

        create_city_label = Label(create_lower_frame, text='City', font=("Courier", 10))
        create_city_label.grid(row=2, column=0, padx=10, pady=10)
        create_city_entry = Entry(create_lower_frame, font=("Courier", 10))
        create_city_entry.grid(row=2, column=1, padx=10, pady=10, sticky='we')

        create_street_label = Label(create_lower_frame, text='Street', font=("Courier", 10))
        create_street_label.grid(row=3, column=0, padx=10, pady=10)
        create_street_entry = Entry(create_lower_frame, font=("Courier", 10))
        create_street_entry.grid(row=3, column=1, padx=10, pady=10, sticky='we')

        create_building_label = Label(create_lower_frame, text='Building', font=("Courier", 10))
        create_building_label.grid(row=4, column=0, padx=10, pady=10)
        create_building_entry = Entry(create_lower_frame, font=("Courier", 10))
        create_building_entry.grid(row=4, column=1, padx=10, pady=10, sticky='we')

        create_apartment_label = Label(create_lower_frame, text='Apartment', font=("Courier", 10))
        create_apartment_label.grid(row=5, column=0, padx=10, pady=10)
        create_apartment_entry = Entry(create_lower_frame, font=("Courier", 10))
        create_apartment_entry.grid(row=5, column=1, padx=10, pady=10, sticky='we')

        # UI LEFT create Buttons
        create_upper_clear = Button(create_upper_frame, text="Clear Fields", fg=button_fg,
                                    activeforeground=button_act_fg,
                                    bg='#ffcc02', activebackground='#e6b802', font=("Courier", 10), borderwidth=1)
        create_upper_clear.grid(row=5, column=0, columnspan=2, padx=10, pady=10, sticky='we')

        create_address_search = Button(create_lower_frame, text="Search", fg=button_fg, activeforeground=button_act_fg,
                                       bg=button_bg, activebackground=button_act_bg, font=("Courier", 10),
                                       borderwidth=1)
        create_address_search.grid(row=7, column=0, columnspan=2, padx=10, pady=10, sticky='we')

        create_lower_clear = Button(create_lower_frame, text="Clear Fields", fg=button_fg,
                                    activeforeground=button_act_fg,
                                    bg='#ffcc02', activebackground='#e6b802', font=("Courier", 10), borderwidth=1)
        create_lower_clear.grid(row=6, column=0, columnspan=2, padx=10, pady=10, sticky='we')

        create_create_record = Button(person_create_window, text="Create Record", fg=button_fg,
                                      activeforeground=button_act_fg, bg='#66cc77',
                                      activebackground='#549960', font=("Courier", 10), borderwidth=1)
        create_create_record.grid(row=3, column=0, columnspan=2, padx=10, pady=10, sticky='we')

        # UI RIGHT Address label
        create_address_label = Label(person_create_window, text='Address', font=("Courier", 12))
        create_address_label.grid(row=0, column=2, columnspan=2, padx=25, pady=10)

        # RIGHT Address list
        # RIGHT Frame base
        create_frame = Frame(person_create_window, bg='#549960', width=600)
        create_frame.grid(row=1, column=2, rowspan=2, padx=10, pady=10, sticky='nsew')
        # RIGHT Canvas
        create_canvas = Canvas(create_frame, bg='#f0f0f0', width=600)
        create_canvas.pack(side=LEFT, fill=BOTH, padx=2, pady=2)

        # RIGHT Scrollbar
        create_scrollbar = ttk.Scrollbar(person_create_window, orient=VERTICAL, command=create_canvas.yview)
        create_scrollbar.grid(row=1, column=3, rowspan=2, sticky='nsew')
        # RIGHT Configure Scrollbar
        # * bind scrollbar "Y scroll" command to canvas
        create_canvas.configure(yscrollcommand=create_scrollbar.set)
        # * * restrict scroll region
        create_canvas.bind('<Configure>', lambda e: create_canvas.configure(scrollregion=create_canvas.bbox('all')))

        # RIGHT Create content frame(window)
        create_content_frame = Frame(create_canvas, bg='#f0f0f0')
        create_canvas.create_window((2, 2), window=create_content_frame, anchor="nw", width=600)
        create_content_frame.grid_columnconfigure(0, weight=1)

        # Def Commands
        def upper_clear():
            create_firstname_entry.delete(0, END)
            create_lastname_entry.delete(0, END)
            create_patronym_entry.delete(0, END)
            create_dateofbirth_entry.delete(0, END)

        def lower_clear():
            create_id_value.config(text="")
            create_city_entry.delete(0, END)
            create_street_entry.delete(0, END)
            create_building_entry.delete(0, END)
            create_apartment_entry.delete(0, END)

        def create_search_addresses():
            try:
                connection = psycopg2.connect(user=connection_user,
                                              password=connection_password,
                                              host=connection_host,
                                              port=connection_port,
                                              database=connection_database)
                cursor = connection.cursor()
                print("Connected to PostgreSQL;")

                # Getting values from addresses fields
                if create_id_value.cget("text"):
                    create_query_id = create_id_value.cget("text")
                else:
                    create_query_id = None

                if create_city_entry.get():
                    create_city_id = create_city_entry.get()
                else:
                    create_city_id = None

                if create_street_entry.get():
                    create_street_id = create_street_entry.get()
                else:
                    create_street_id = None

                if create_building_entry.get():
                    create_building_id = create_building_entry.get()
                else:
                    create_building_id = None

                if create_apartment_entry.get():
                    create_apartment_id = create_apartment_entry.get()
                else:
                    create_apartment_id = None

                # PostgreSQL command
                query = """
                            SELECT * FROM address
                            WHERE (city = %(city)s OR %(city)s IS NULL)
                            AND (street = %(street)s OR %(street)s IS NULL)
                            AND (building = %(building)s OR %(building)s IS NULL)
                            AND (apartment = %(apartment)s OR %(apartment)s IS NULL)
                        """
                # Legacy code chunk
                # SELECT * FROM address
                # WHERE (ID = %(ID)s OR %(ID)s IS NULL)
                # AND (city = %(city)s OR %(city)s IS NULL)
                # AND (street = %(street)s OR %(street)s IS NULL)
                # AND (building = %(building)s OR %(building)s IS NULL)
                # AND (apartment = %(apartment)s OR %(apartment)s IS NULL)

                parameters = dict(ID=create_query_id, city=create_city_id, street=create_street_id,
                                  building=create_building_id, apartment=create_apartment_id)
                cursor.execute(query, parameters)
                print("Executing PostgreSQL query")

                # Fetch info into result
                result = cursor.fetchall()
                print("Result:", result)

                # Destroying(!) previous result
                for widget in create_content_frame.winfo_children():
                    widget.destroy()
                # Placing result in window as rows of buttons
                for index, element in enumerate(result):
                    Button(
                        create_content_frame, text=f'{element[0]}, {element[1]}, {element[2]}, {element[3]},'
                                                   f' ap. {element[4]}', anchor="w",
                        command=lambda lamb_id=element[0], lamb_city=element[1], lamb_street=element[2],
                        lamb_building=element[3], lamb_apartment=element[4]:
                        [
                            create_id_value.config(text=""), create_id_value.config(text=f"{lamb_id}"),
                            create_city_entry.delete(0, END), create_city_entry.insert(0, lamb_city),
                            create_street_entry.delete(0, END), create_street_entry.insert(0, lamb_street),
                            create_building_entry.delete(0, END), create_building_entry.insert(0, lamb_building),
                            create_apartment_entry.delete(0, END), create_apartment_entry.insert(0, lamb_apartment)
                        ],
                        bg="#FFFFFF",
                        activebackground=button_bg,
                        borderwidth=1
                        ).grid(row=index, column=0, sticky='nsew', padx=1, pady=1)

            except (Exception, psycopg2.Error) as error:
                print("Error while connecting to PostgreSQL: ", error)
            finally:
                # noinspection PyUnboundLocalVariable
                if connection:
                    # noinspection PyUnboundLocalVariable
                    cursor.close()
                    # noinspection PyUnboundLocalVariable
                    connection.close()
                    print("PostgreSQL connection is closed.")

        def create_insert_person():
            try:
                connection = psycopg2.connect(user=connection_user,
                                              password=connection_password,
                                              host=connection_host,
                                              port=connection_port,
                                              database=connection_database)
                cursor = connection.cursor()
                print("Connected to PostgreSQL;")

                # Check if person entries are filled
                if create_firstname_entry.get():
                    insert_firstname_query = create_firstname_entry.get()
                else:
                    messagebox.showerror("Error", "Please, enter correct firstname")
                    return

                if create_lastname_entry.get():
                    insert_lastname_query = create_lastname_entry.get()
                else:
                    messagebox.showerror("Error", "Please, enter correct lastname")
                    return

                if create_patronym_entry.get():
                    insert_patronym_query = create_patronym_entry.get()
                else:
                    insert_patronym_query = None

                if create_dateofbirth_entry.get():
                    insert_dateofbirth_query = create_dateofbirth_entry.get()
                else:
                    messagebox.showerror("Error", "Please, enter correct date of birth")
                    return

                # Check if Address is present
                if create_id_value.cget("text"):
                    insert_addressid_query = create_id_value.cget("text")
                else:
                    messagebox.showerror("Error", "Please, choose address id")
                    return

                # Confirm insert
                ask = messagebox.askyesno("Are you sure?", f"Are you sure you want to add {insert_firstname_query}?")
                if ask:
                    pass
                else:
                    return

                # PostgreSQL command
                query = """
                            INSERT INTO person (firstname, lastname, patronym, dateofbirth, addressid) VALUES
                            (%(firstname)s, %(lastname)s, %(patronym)s, %(dateofbirth)s, %(addressid)s)
                        """
                parameters = dict(firstname=insert_firstname_query, lastname=insert_lastname_query,
                                  patronym=insert_patronym_query, dateofbirth=insert_dateofbirth_query,
                                  addressid=insert_addressid_query)
                cursor.execute(query, parameters)
                connection.commit()

            except (Exception, psycopg2.Error) as error:
                print("Error while connecting to PostgreSQL: ", error)
            finally:
                # noinspection PyUnboundLocalVariable
                if connection:
                    # noinspection PyUnboundLocalVariable
                    cursor.close()
                    # noinspection PyUnboundLocalVariable
                    connection.close()
                    print("PostgreSQL connection is closed.")

        # Add commands to buttons
        create_upper_clear.configure(command=lambda: upper_clear())
        create_lower_clear.configure(command=lambda: lower_clear())
        create_address_search.configure(command=lambda: create_search_addresses())
        create_create_record.configure(command=lambda: create_insert_person())

    def person_delete():
        # Get ID from person window
        if person_id_entry.get():
            get_person_id = person_id_entry.get()
        else:
            messagebox.showerror("Warning!", "No ID is present!")
            return

        # Check if ID valid
        try:
            id_management_connection = psycopg2.connect(user=connection_user,
                                                        password=connection_password,
                                                        host=connection_host,
                                                        port=connection_port,
                                                        database=connection_database)
            id_management_cursor = id_management_connection.cursor()
            print("Connected to PostgreSQL;")

            # Postgres command
            id_management_query = """
                            SELECT * FROM person WHERE ID = %(ID)s
                                  """
            id_management_parameters = dict(ID=get_person_id)
            id_management_cursor.execute(id_management_query, id_management_parameters)
            id_management_value = id_management_cursor.fetchall()
            print(id_management_value)
            if id_management_value:
                pass
            else:
                messagebox.showerror("Error!", "The ID is invalid!")
                return

        except (Exception, psycopg2.Error) as id_management_error:
            print("Error while connecting to PostgreSQL: ", id_management_error)
            messagebox.showerror("Error!", "UNKNOWN ERROR")
        finally:
            # noinspection PyUnboundLocalVariable
            if id_management_connection:
                # noinspection PyUnboundLocalVariable
                id_management_cursor.close()
                # noinspection PyUnboundLocalVariable
                id_management_connection.close()
                print("PostgreSQL connection is closed.")

        # Delete command
        try:
            connection = psycopg2.connect(user=connection_user,
                                          password=connection_password,
                                          host=connection_host,
                                          port=connection_port,
                                          database=connection_database)
            cursor = connection.cursor()
            print("Connected to PostgreSQL;")

            # Confirm update
            ask = messagebox.askyesno("Confirm", f"Are you sure you want to delete {person_firstname_entry.get()} "
                                                 f"{person_lastname_entry.get()}?")
            if ask:
                pass
            else:
                return

            # PostgreSQL command
            query = """
                        DELETE FROM person
                        WHERE ID = %(ID)s
                    """
            parameters = dict(ID=get_person_id)
            cursor.execute(query, parameters)
            connection.commit()

        except (Exception, psycopg2.Error) as delete_error:
            print("Error while connecting to PostgreSQL: ", delete_error)
        finally:
            # noinspection PyUnboundLocalVariable
            if connection:
                # noinspection PyUnboundLocalVariable
                cursor.close()
                # noinspection PyUnboundLocalVariable
                connection.close()
                print("PostgreSQL connection is closed.")

    # Add commands to buttons
    person_clear_button.configure(command=lambda: person_clear())
    person_search_button.configure(command=lambda: person_search())
    person_edit_button.configure(command=lambda: person_edit())
    person_create_button.configure(command=lambda: person_create())
    person_delete_button.configure(command=lambda: person_delete())


def choose_address():
    # Address Window
    address_window = Toplevel()
    address_window.title('Address')
    address_window.iconbitmap('media/database.ico')
    address_window.geometry('980x660')
    address_window.resizable(False, False)
    address_window.focus_force()

    # Opening management
    root.state('withdrawn')

    # Closing management
    def close_address():
        address_window.destroy()
        root.state('normal')
        root.focus_force()

    # Closing protocol
    address_window.protocol("WM_DELETE_WINDOW", close_address)

    # LEFT Address UI labels and entries
    address_label = Label(address_window, text='Address', font=("Courier", 12))
    address_label.grid(row=0, column=0, columnspan=2, padx=25, pady=10)

    address_id_label = Label(address_window, text='ID', font=("Courier", 10))
    address_id_label.grid(row=1, column=0, padx=10, pady=10)
    address_id_entry = Entry(address_window, font=("Courier", 10))
    address_id_entry.grid(row=1, column=1, padx=10, pady=10)

    address_city_label = Label(address_window, text='City', font=("Courier", 10))
    address_city_label.grid(row=2, column=0, padx=10, pady=10)
    address_city_entry = Entry(address_window, font=("Courier", 10))
    address_city_entry.grid(row=2, column=1, padx=10, pady=10)

    address_street_label = Label(address_window, text='Street', font=("Courier", 10))
    address_street_label.grid(row=3, column=0, padx=10, pady=10)
    address_street_entry = Entry(address_window, font=("Courier", 10))
    address_street_entry.grid(row=3, column=1, padx=10, pady=10)

    address_building_label = Label(address_window, text='Building', font=("Courier", 10))
    address_building_label.grid(row=4, column=0, padx=10, pady=10)
    address_building_entry = Entry(address_window, font=("Courier", 10))
    address_building_entry.grid(row=4, column=1, padx=10, pady=10)

    address_apartment_label = Label(address_window, text='Apartment', font=("Courier", 10))
    address_apartment_label.grid(row=5, column=0, padx=10, pady=10)
    address_apartment_entry = Entry(address_window, font=("Courier", 10))
    address_apartment_entry.grid(row=5, column=1, padx=10, pady=10)

    # LEFT Person UI buttons
    address_clear_button = Button(address_window, text="Clear Fields", fg=button_fg, activeforeground=button_act_fg,
                                  bg='#ffcc02', activebackground='#e6b802', font=("Courier", 10), borderwidth=1)
    address_clear_button.grid(row=6, column=0, columnspan=2, padx=10, pady=10, sticky='we')

    address_search_button = Button(address_window, text="Search", fg=button_fg, activeforeground=button_act_fg,
                                   bg=button_bg, activebackground=button_act_bg, font=("Courier", 10), borderwidth=1)
    address_search_button.grid(row=7, column=0, columnspan=2, padx=10, pady=10, sticky='we')

    address_edit_button = Button(address_window, text="Edit", fg=button_fg, activeforeground=button_act_fg,
                                 bg='#6677cc', activebackground='#546099', font=("Courier", 10), borderwidth=1)
    address_edit_button.grid(row=8, column=0, columnspan=2, padx=10, pady=10, sticky='we')

    address_create_button = Button(address_window, text="Create New", fg=button_fg, activeforeground=button_act_fg,
                                   bg='#66cc77', activebackground='#549960', font=("Courier", 10), borderwidth=1)
    address_create_button.grid(row=9, column=0, columnspan=2, padx=10, pady=10, sticky='we')

    address_delete_button = Button(address_window, text="Delete", fg=button_fg, activeforeground=button_act_fg,
                                   bg='#c85a50', activebackground='#ae4137', font=("Courier", 10), borderwidth=1)
    address_delete_button.grid(row=10, column=0, columnspan=2, padx=10, pady=10, sticky='we')

    # LEFT empty spaces
    empty_space_11 = Label(address_window, text='')
    empty_space_11.grid(row=11, column=0, padx=10, pady=40)

    # RIGHT Addresses UI label
    people_label = Label(address_window, text='Addresses', font=("Courier", 12))
    people_label.grid(row=0, column=2, columnspan=2, padx=25, pady=10)

    # RIGHT list of addresses
    # RIGHT Frame base
    address_frame = Frame(address_window, bg='#6b6b6b', width=600)
    address_frame.grid(row=1, column=2, rowspan=11, padx=10, pady=10, sticky='nsew')
    # RIGHT Canvas
    address_canvas = Canvas(address_frame, bg='#f0f0f0', width=600)
    address_canvas.pack(side=LEFT, fill=BOTH, padx=2, pady=2)

    # RIGHT Scrollbar
    address_scrollbar = ttk.Scrollbar(address_window, orient=VERTICAL, command=address_canvas.yview)
    address_scrollbar.grid(row=1, column=3, rowspan=11, sticky='nsew')
    # RIGHT Configure Scrollbar
    # ! bind scrollbar "Y scroll" command to canvas
    address_canvas.configure(yscrollcommand=address_scrollbar.set)
    # ! ! restrict scroll region
    address_canvas.bind('<Configure>', lambda e: address_canvas.configure(scrollregion=address_canvas.bbox('all')))

    # RIGHT Create content frame(window)
    content_frame = Frame(address_canvas, bg='#f0f0f0')
    address_canvas.create_window((2, 2), window=content_frame, anchor="nw", width=600)
    content_frame.grid_columnconfigure(0, weight=1)

    # Commands for buttons
    def address_clear():
        address_id_entry.delete(0, END)
        address_city_entry.delete(0, END)
        address_street_entry.delete(0, END)
        address_building_entry.delete(0, END)
        address_apartment_entry.delete(0, END)

    def address_search():
        try:
            connection = psycopg2.connect(user=connection_user,
                                          password=connection_password,
                                          host=connection_host,
                                          port=connection_port,
                                          database=connection_database)
            cursor = connection.cursor()
            print("Connected to PostgreSQL;")

            # Getting column values from entries
            if address_id_entry.get():
                query_id = address_id_entry.get()
            else:
                query_id = None

            if address_city_entry.get():
                query_city = address_city_entry.get()
            else:
                query_city = None

            if address_street_entry.get():
                query_street = address_street_entry.get()
            else:
                query_street = None

            if address_building_entry.get():
                query_building = address_building_entry.get()
            else:
                query_building = None

            if address_apartment_entry.get():
                query_apartment = address_apartment_entry.get()
            else:
                query_apartment = None

            # PostgreSQL command
            query = """
                        SELECT * FROM address
                        WHERE (ID = %(ID)s OR %(ID)s IS NULL)
                        AND (city = %(city)s OR %(city)s IS NULL)
                        AND (street = %(street)s OR %(street)s IS NULL)
                        AND (building = %(building)s OR %(building)s IS NULL)
                        AND (apartment = %(apartment)s OR %(apartment)s IS NULL)
                    """
            parameters = dict(ID=query_id, city=query_city, street=query_street,
                              building=query_building, apartment=query_apartment)
            cursor.execute(query, parameters)

            print("Executing PostgreSQL query")
            result = cursor.fetchall()
            print("Result:", result)

            # Destroying(!) previous result
            for widget in content_frame.winfo_children():
                widget.destroy()
            # Checking if patronym exists
            for index, element in enumerate(result):
                # Placing result in window as rows of buttons
                Button(
                    content_frame, text=f'{element[0]}, {element[1]}, {element[2]} {element[3]}, ap. {element[4]}',
                                        anchor="w",
                    command=lambda lamb_id=element[0], lamb_city=element[1], lamb_street=element[2],
                    lamb_building=element[3], lamb_apartment=element[4]:
                    [
                        address_id_entry.delete(0, END), address_id_entry.insert(0, lamb_id),
                        address_city_entry.delete(0, END), address_city_entry.insert(0, lamb_city),
                        address_street_entry.delete(0, END), address_street_entry.insert(0, lamb_street),
                        address_building_entry.delete(0, END), address_building_entry.insert(0, lamb_building),
                        address_apartment_entry.delete(0, END), address_apartment_entry.insert(0, lamb_apartment)
                    ],
                    bg="#FFFFFF",
                    activebackground=button_bg,
                    borderwidth=1
                    ).grid(row=index, column=0, sticky='nsew', padx=1, pady=1)

        except (Exception, psycopg2.Error) as error:
            print("Error while connecting to PostgreSQL: ", error)
        finally:
            # noinspection PyUnboundLocalVariable
            if connection:
                # noinspection PyUnboundLocalVariable
                cursor.close()
                # noinspection PyUnboundLocalVariable
                connection.close()
                print("PostgreSQL connection is closed.")

    def address_edit():
        # Get ID from address window
        if address_id_entry.get():
            get_address_id = address_id_entry.get()
        else:
            messagebox.showerror("Warning!", "No ID is present!")
            return

        # Check if ID is valid
        try:
            id_management_connection = psycopg2.connect(user=connection_user,
                                                        password=connection_password,
                                                        host=connection_host,
                                                        port=connection_port,
                                                        database=connection_database)
            id_management_cursor = id_management_connection.cursor()
            print("Connected to PostgreSQL;")

            # Postgres command
            id_management_query = """
                            SELECT * FROM address WHERE ID = %(ID)s
                                  """
            id_management_parameters = dict(ID=get_address_id)
            id_management_cursor.execute(id_management_query, id_management_parameters)
            id_management_value = id_management_cursor.fetchall()
            print(id_management_value)
            if id_management_value:
                pass
            else:
                messagebox.showerror("Error!", "The ID is invalid!")
                return

        except (Exception, psycopg2.Error) as id_management_error:
            print("Error while connecting to PostgreSQL: ", id_management_error)
            messagebox.showerror("Error!", "UNKNOWN ERROR")
        finally:
            # noinspection PyUnboundLocalVariable
            if id_management_connection:
                # noinspection PyUnboundLocalVariable
                id_management_cursor.close()
                # noinspection PyUnboundLocalVariable
                id_management_connection.close()
                print("PostgreSQL connection is closed.")
        
        # Address edit window
        address_edit_window = Toplevel()
        address_edit_window.title('Edit')
        address_edit_window.iconbitmap('media/database.ico')
        address_edit_window.geometry('340x380')
        address_edit_window.resizable(False, False)
        address_edit_window.focus_force()

        # Opening management
        address_window.state('withdrawn')

        # Closing management
        def close_address_edit():
            address_edit_window.destroy()
            address_window.state('normal')
            address_window.focus_force()

        # Closing protocol
        address_edit_window.protocol("WM_DELETE_WINDOW", close_address_edit)

        # UI Labels and Entries
        edit_address_label = Label(address_edit_window, text='Edit Address', font=("Courier", 12))
        edit_address_label.grid(row=0, column=0, columnspan=2, padx=25, pady=10)

        edit_address_id_label = Label(address_edit_window, text='ID', font=("Courier", 10))
        edit_address_id_label.grid(row=1, column=0, padx=10, pady=10)
        edit_address_id_value = Label(address_edit_window, text="", font=("Courier", 10),
                                      anchor='w', background='#f0f0f0', borderwidth=1, relief='sunken', width=24)
        edit_address_id_value.grid(row=1, column=1, padx=10, pady=10)

        edit_city_label = Label(address_edit_window, text='City', font=("Courier", 10))
        edit_city_label.grid(row=2, column=0, padx=10, pady=10)
        edit_city_entry = Entry(address_edit_window, font=("Courier", 10))
        edit_city_entry.grid(row=2, column=1, padx=10, pady=10, sticky='we')

        edit_street_label = Label(address_edit_window, text='Street', font=("Courier", 10))
        edit_street_label.grid(row=3, column=0, padx=10, pady=10)
        edit_street_entry = Entry(address_edit_window, font=("Courier", 10))
        edit_street_entry.grid(row=3, column=1, padx=10, pady=10, sticky='we')

        edit_building_label = Label(address_edit_window, text='Building', font=("Courier", 10))
        edit_building_label.grid(row=4, column=0, padx=10, pady=10)
        edit_building_entry = Entry(address_edit_window, font=("Courier", 10))
        edit_building_entry.grid(row=4, column=1, padx=10, pady=10, sticky='we')

        edit_apartment_label = Label(address_edit_window, text='Apartment', font=("Courier", 10))
        edit_apartment_label.grid(row=5, column=0, padx=10, pady=10)
        edit_apartment_entry = Entry(address_edit_window, font=("Courier", 10))
        edit_apartment_entry.grid(row=5, column=1, padx=10, pady=10, sticky='we')

        # UI Buttons
        edit_clear = Button(address_edit_window, text="Clear Fields", fg=button_fg, activeforeground=button_act_fg,
                            bg='#ffcc02', activebackground='#e6b802', font=("Courier", 10), borderwidth=1)
        edit_clear.grid(row=6, column=0, columnspan=2, padx=10, pady=10, sticky='we')

        edit_edit_record = Button(address_edit_window, text="Update Record", fg=button_fg,
                                  activeforeground=button_act_fg, bg='#6677cc',
                                  activebackground='#546099', font=("Courier", 10), borderwidth=1)
        edit_edit_record.grid(row=7, column=0, columnspan=2, padx=10, pady=10, sticky='we')

        # Def Commands
        def clear():
            edit_city_entry.delete(0, END)
            edit_street_entry.delete(0, END)
            edit_building_entry.delete(0, END)
            edit_apartment_entry.delete(0, END)

        def edit_update_address():
            try:
                connection = psycopg2.connect(user=connection_user,
                                              password=connection_password,
                                              host=connection_host,
                                              port=connection_port,
                                              database=connection_database)
                cursor = connection.cursor()
                print("Connected to PostgreSQL;")

                # Check if address entries are filled
                if edit_address_id_value.cget("text"):
                    update_id_query = edit_address_id_value.cget("text")
                else:
                    messagebox.showerror("Warning!", "No valid ID is present!")
                    return

                if edit_city_entry.get():
                    update_city_query = edit_city_entry.get()
                else:
                    messagebox.showerror("Error", "Please, enter correct city")
                    return

                if edit_street_entry.get():
                    update_street_query = edit_street_entry.get()
                else:
                    messagebox.showerror("Error", "Please, enter correct street")
                    return

                if edit_building_entry.get():
                    update_building_query = edit_building_entry.get()
                else:
                    messagebox.showerror("Error", "Please, enter correct building")
                    return

                if edit_apartment_entry.get():
                    update_apartment_query = edit_apartment_entry.get()
                else:
                    messagebox.showerror("Error", "Please, enter correct apartment")
                    return

                # Confirm update
                ask = messagebox.askyesno("Confirm", "Apply Changes?")
                if ask:
                    pass
                else:
                    return

                # PostgreSQL command
                query = """
                            UPDATE address SET
                            city = %(city)s, street = %(street)s, building = %(building)s, apartment = %(apartment)s
                            WHERE ID = %(ID)s
                        """
                parameters = dict(city=update_city_query, street=update_street_query,
                                  building=update_building_query, apartment=update_apartment_query,
                                  ID=update_id_query)
                cursor.execute(query, parameters)
                connection.commit()

            except (Exception, psycopg2.Error) as updating_error:
                print("Error while connecting to PostgreSQL: ", updating_error)
            finally:
                # noinspection PyUnboundLocalVariable
                if connection:
                    # noinspection PyUnboundLocalVariable
                    cursor.close()
                    # noinspection PyUnboundLocalVariable
                    connection.close()
                    print("PostgreSQL connection is closed.")

        # Add commands to buttons
        edit_clear.configure(command=lambda: clear())
        edit_edit_record.configure(command=lambda: edit_update_address())

        # Insert data according to valid ID (Post-window-creation fields filling)
        try:
            id_management_connection = psycopg2.connect(user=connection_user,
                                                        password=connection_password,
                                                        host=connection_host,
                                                        port=connection_port,
                                                        database=connection_database)
            id_management_cursor = id_management_connection.cursor()
            print("Connected to PostgreSQL;")

            # PostgreSQL command to eject data
            id_management_query = """
                                    SELECT * FROM address
                                    WHERE ID = %(ID)s
                                  """
            id_management_parameters = dict(ID=get_address_id)
            id_management_cursor.execute(id_management_query, id_management_parameters)
            id_management_result = id_management_cursor.fetchone()

            # Insert address info into entries
            edit_address_id_value.config(text=f"{id_management_result[0]}")
            edit_city_entry.insert(0, id_management_result[1])
            edit_street_entry.insert(0, id_management_result[2])
            edit_building_entry.insert(0, id_management_result[3])
            edit_apartment_entry.insert(0, id_management_result[4])

        except (Exception, psycopg2.Error) as error:
            print("Error while connecting to PostgreSQL: ", error)
        finally:
            # noinspection PyUnboundLocalVariable
            if id_management_connection:
                # noinspection PyUnboundLocalVariable
                id_management_cursor.close()
                # noinspection PyUnboundLocalVariable
                id_management_connection.close()
                print("PostgreSQL connection is closed.")

    def address_create():
        # Address create window
        address_create_window = Toplevel()
        address_create_window.title('Create')
        address_create_window.iconbitmap('media/database.ico')
        address_create_window.geometry('340x380')
        address_create_window.resizable(False, False)
        address_create_window.focus_force()

        # Opening management
        address_window.state('withdrawn')

        # Closing management
        def close_address_create():
            address_create_window.destroy()
            address_window.state('normal')
            address_window.focus_force()

        # Closing protocol
        address_create_window.protocol("WM_DELETE_WINDOW", close_address_create)

        # UI Labels and Entries
        create_address_label = Label(address_create_window, text='Create Address', font=("Courier", 12))
        create_address_label.grid(row=0, column=0, columnspan=2, padx=25, pady=10)

        create_city_label = Label(address_create_window, text='City', font=("Courier", 10))
        create_city_label.grid(row=2, column=0, padx=10, pady=10)
        create_city_entry = Entry(address_create_window, font=("Courier", 10))
        create_city_entry.grid(row=2, column=1, padx=10, pady=10, sticky='we')

        create_street_label = Label(address_create_window, text='Street', font=("Courier", 10))
        create_street_label.grid(row=3, column=0, padx=10, pady=10)
        create_street_entry = Entry(address_create_window, font=("Courier", 10))
        create_street_entry.grid(row=3, column=1, padx=10, pady=10, sticky='we')

        create_building_label = Label(address_create_window, text='Building', font=("Courier", 10))
        create_building_label.grid(row=4, column=0, padx=10, pady=10)
        create_building_entry = Entry(address_create_window, font=("Courier", 10))
        create_building_entry.grid(row=4, column=1, padx=10, pady=10, sticky='we')

        create_apartment_label = Label(address_create_window, text='Apartment', font=("Courier", 10))
        create_apartment_label.grid(row=5, column=0, padx=10, pady=10)
        create_apartment_entry = Entry(address_create_window, font=("Courier", 10))
        create_apartment_entry.grid(row=5, column=1, padx=10, pady=10, sticky='we')

        # UI Buttons
        create_clear = Button(address_create_window, text="Clear Fields", fg=button_fg, activeforeground=button_act_fg,
                              bg='#ffcc02', activebackground='#e6b802', font=("Courier", 10), borderwidth=1)
        create_clear.grid(row=6, column=0, columnspan=2, padx=10, pady=10, sticky='we')

        create_create_record = Button(address_create_window, text="Create Record", fg=button_fg,
                                      activeforeground=button_act_fg, bg='#66cc77',
                                      activebackground='#549960', font=("Courier", 10), borderwidth=1)
        create_create_record.grid(row=7, column=0, columnspan=2, padx=10, pady=10, sticky='we')

        # Def Commands
        def clear():
            create_city_entry.delete(0, END)
            create_street_entry.delete(0, END)
            create_building_entry.delete(0, END)
            create_apartment_entry.delete(0, END)

        def create_insert_address():
            try:
                connection = psycopg2.connect(user=connection_user,
                                              password=connection_password,
                                              host=connection_host,
                                              port=connection_port,
                                              database=connection_database)
                cursor = connection.cursor()
                print("Connected to PostgreSQL;")

                # Check if address entries are filled
                if create_city_entry.get():
                    insert_city_query = create_city_entry.get()
                else:
                    messagebox.showerror("Error", "Please, enter correct city")
                    return

                if create_street_entry.get():
                    insert_street_query = create_street_entry.get()
                else:
                    messagebox.showerror("Error", "Please, enter correct street")
                    return

                if create_building_entry.get():
                    insert_building_query = create_building_entry.get()
                else:
                    messagebox.showerror("Error", "Please, enter correct building")
                    return

                if create_apartment_entry.get():
                    insert_apartment_query = create_apartment_entry.get()
                else:
                    messagebox.showerror("Error", "Please, enter correct apartment")
                    return

                # Confirm insert
                ask = messagebox.askyesno("Confirm", "Create address?")
                if ask:
                    pass
                else:
                    return

                # PostgreSQL command
                query = """
                            INSERT INTO address (city, street, building, apartment) VALUES
                            (%(city)s, %(street)s, %(building)s, %(apartment)s)
                        """
                parameters = dict(city=insert_city_query, street=insert_street_query,
                                  building=insert_building_query, apartment=insert_apartment_query)
                cursor.execute(query, parameters)
                connection.commit()

            except (Exception, psycopg2.Error) as updating_error:
                print("Error while connecting to PostgreSQL: ", updating_error)
            finally:
                # noinspection PyUnboundLocalVariable
                if connection:
                    # noinspection PyUnboundLocalVariable
                    cursor.close()
                    # noinspection PyUnboundLocalVariable
                    connection.close()
                    print("PostgreSQL connection is closed.")

        # Add commands to buttons
        create_clear.configure(command=lambda: clear())
        create_create_record.configure(command=lambda: create_insert_address())

    def address_delete():
        # Get ID from address window
        if address_id_entry.get():
            get_address_id = address_id_entry.get()
        else:
            messagebox.showerror("Warning!", "No ID is present!")
            return

        # Check if ID valid
        try:
            id_management_connection = psycopg2.connect(user=connection_user,
                                                        password=connection_password,
                                                        host=connection_host,
                                                        port=connection_port,
                                                        database=connection_database)
            id_management_cursor = id_management_connection.cursor()
            print("Connected to PostgreSQL;")

            # Postgres command
            id_management_query = """
                            SELECT * FROM address WHERE ID = %(ID)s
                                  """
            id_management_parameters = dict(ID=get_address_id)
            id_management_cursor.execute(id_management_query, id_management_parameters)
            id_management_value = id_management_cursor.fetchall()
            print(id_management_value)
            if id_management_value:
                pass
            else:
                messagebox.showerror("Error!", "The ID is invalid!")
                return

        except (Exception, psycopg2.Error) as id_management_error:
            print("Error while connecting to PostgreSQL: ", id_management_error)
            messagebox.showerror("Error!", "UNKNOWN ERROR")
        finally:
            # noinspection PyUnboundLocalVariable
            if id_management_connection:
                # noinspection PyUnboundLocalVariable
                id_management_cursor.close()
                # noinspection PyUnboundLocalVariable
                id_management_connection.close()
                print("PostgreSQL connection is closed.")

        # Delete command
        try:
            connection = psycopg2.connect(user=connection_user,
                                          password=connection_password,
                                          host=connection_host,
                                          port=connection_port,
                                          database=connection_database)
            cursor = connection.cursor()
            print("Connected to PostgreSQL;")

            # Confirm update
            ask = messagebox.askyesno("Confirm", "Are you sure you want to delete this address?")
            if ask:
                pass
            else:
                return

            # PostgreSQL command
            query = """
                        DELETE FROM address
                        WHERE ID = %(ID)s
                    """
            parameters = dict(ID=get_address_id)
            cursor.execute(query, parameters)
            connection.commit()

        except (Exception, psycopg2.Error) as delete_error:
            print("Error while connecting to PostgreSQL: ", delete_error)
        finally:
            # noinspection PyUnboundLocalVariable
            if connection:
                # noinspection PyUnboundLocalVariable
                cursor.close()
                # noinspection PyUnboundLocalVariable
                connection.close()
                print("PostgreSQL connection is closed.")

    # Add commands to buttons
    address_clear_button.configure(command=lambda: address_clear())
    address_search_button.configure(command=lambda: address_search())
    address_edit_button.configure(command=lambda: address_edit())
    address_create_button.configure(command=lambda: address_create())
    address_delete_button.configure(command=lambda: address_delete())


# Root UI
label_hello = Label(root, text="Hello, what would you like to view?", font=("Courier", 14))
label_hello.place(x=225, y=125)

button_root_person = Button(root, text="Person", fg=button_fg, activeforeground=button_act_fg, bg=button_bg,
                            activebackground=button_act_bg, width=20, height=3, font=("Courier", 14),
                            command=lambda: choose_person(), borderwidth=1)
button_root_person.place(x=175, y=225)

button_root_address = Button(root, text="Address", fg=button_fg, activeforeground=button_act_fg, bg=button_bg,
                             activebackground=button_act_bg, width=20, height=3, font=("Courier", 14),
                             command=lambda: choose_address(), borderwidth=1)
button_root_address.place(x=425, y=225)

login_function()

root.mainloop()
