import streamlit as st
#import mysql.connector
import sqlite3
from datetime import datetime
import pandas as pd
import requests
from streamlit_lottie import st_lottie
import streamlit as st
import streamlit.components.v1 as components
import htmlComponents
from scheduleFlights import schedule_new_flights
from manage_booking import filter_search_bookings

# for my sql workbench
# config = {
#     'user': 'root',
#     'password': 'Helloworld@123',
#     'host': 'localhost',
#     'port': 3306,  # Update the port number to 3305 because in installation i gave port 3305
#     'database': 'airlines'
# }


def loti(url):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    else:
        return r.json()


def create_connection():
    """Create a connection to the MySQL database."""
    #db = mysql.connector.connect(**config)
    db=sqlite3.connect('setup/airlines.db')
    return db


def create_database(db):
    """Create the 'userdb' database if it doesn't exist."""
    cursor = db.cursor()
    cursor.execute("CREATE DATABASE IF NOT EXISTS userdb")
    cursor.close()


def create_patients_table(db):
    """Create the patients table in the database."""
    cursor = db.cursor()

    create_patients_table_query = """
    CREATE TABLE IF NOT EXISTS patients (
        id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(255) NOT NULL,
        age INT,
        contact_number VARCHAR,
        address VARCHAR(255),
        date_added TIMESTAMP DEFAULT CURRENT_TIMESTAMPCHAR(20),
        email VARCHAR(255),
    )
    """

    cursor.execute(create_patients_table_query)
    db.commit()
    st.write("Patients table created successfully.")


def modify_patients_table(db):
    cursor = db.cursor()

    alter_table_query = """
    ALTER TABLE patients
    ADD COLUMN doctor_name VARCHAR(255),
    ADD COLUMN disease VARCHAR(255),
    ADD COLUMN fee INTEGER(5),
    ADD COLUMN tests VARCHAR(255),
    ADD COLUMN cnic VARCHAR(20)
    """

    cursor.execute(alter_table_query)
    db.commit()
    st.write("Patients table modified successfully.")


def create_appointments_table(db):
    """Create the appointments table in the database."""
    cursor = db.cursor()

    create_appointments_table_query = """
    CREATE TABLE IF NOT EXISTS appointments (
        id INT AUTO_INCREMENT PRIMARY KEY,
        patient_id INT,
        appointment_date DATE,
        appointment_time TIME,
        doctor_name VARCHAR(255),
        notes TEXT,
        FOREIGN KEY (patient_id) REFERENCES patients(id)
    )
    """

    cursor.execute(create_appointments_table_query)
    db.commit()
    st.write("Appointments table created successfully.")


def insert_patient_record(db, name, age, contact_number, email, address):
    """Insert a new patient record into the 'patients' table."""
    cursor = db.cursor()

    # Select the database
    cursor.execute("USE userdb")

    insert_patient_query = """
    INSERT INTO patients (name, age, contact_number, email, address)
    VALUES (%s, %s, %s, %s, %s)
    """

    patient_data = (name, age, contact_number, email, address)

    cursor.execute(insert_patient_query, patient_data)
    db.commit()
    st.write("Patient record inserted successfully.")


def fetch_all_flights(db):
    """Fetch all records from the 'Flight_Schedule' table."""
    cursor = db.cursor()

    # Fetch all flights schedule
    select_flight_query = "SELECT FlID,FlightDate,Departure,Arrival,Aircraft,Airport, Destination FROM Flight_Schedule f inner join AirFare a on f.NetFare=a.AfID inner join Route r on a.Route=r.RtID"
    cursor.execute(select_flight_query)
    flights = cursor.fetchall()
    return flights


def fetch_patient_by_id(db, patient_id):
    """Fetch a patient's record from the 'patients' table based on ID."""
    cursor = db.cursor()

    # Select the database
    cursor.execute("USE userdb")

    # Fetch the patient by ID
    select_patient_query = "SELECT * FROM patients WHERE id = %s"
    cursor.execute(select_patient_query, (patient_id,))
    patient = cursor.fetchone()

    return patient


def fetch_patient_by_contact(db, contact_number):
    """Fetch a patient's record from the 'patients' table based on contact number."""
    cursor = db.cursor()

    # Select the database
    cursor.execute("USE userdb")

    # Fetch the patient by contact number
    select_patient_query = "SELECT * FROM patients WHERE contact_number = %s"
    cursor.execute(select_patient_query, (contact_number,))
    patient = cursor.fetchone()

    return patient


def fetch_patient_by_cnis(db, cnis):
    """Fetch a patient's record from the 'patients' table based on CNIS."""
    cursor = db.cursor()

    # Select the database
    cursor.execute("USE userdb")

    # Fetch the patient by CNIS
    select_patient_query = "SELECT * FROM patients WHERE cnis = %s"
    cursor.execute(select_patient_query, (cnis,))
    patient = cursor.fetchone()

    return patient


def delete_patient_record(db, delete_option, delete_value):
    """Delete a patient record from the 'patients' table based on ID, name, or contact number."""
    cursor = db.cursor()

    # Select the database
    cursor.execute("USE userdb")

    # Delete the patient record
    if delete_option == "ID":
        delete_patient_query = "DELETE FROM patients WHERE id = %s"
    elif delete_option == "Name":
        delete_patient_query = "DELETE FROM patients WHERE name = %s"
    elif delete_option == "Contact Number":
        delete_patient_query = "DELETE FROM patients WHERE contact_number = %s"

    cursor.execute(delete_patient_query, (delete_value,))
    db.commit()
    st.write("Patient record deleted successfully.")


def insert_appointment_record(db, patient_id, appointment_date, appointment_time, doctor_name, notes):
    """Insert a new appointment record into the 'appointments' table."""
    cursor = db.cursor()

    # Select the database
    cursor.execute("USE userdb")
    appointment_time = appointment_time.strftime("%H:%M:%S")
    appointment_date = appointment_date.strftime("%Y-%m-%d")
    insert_appointment_query = """
    INSERT INTO appointments (patient_id, appointment_date, appointment_time, doctor_name, notes)
    VALUES (%s, %s, %s, %s, %s)
    """

    appointment_data = (patient_id, appointment_date, appointment_time, doctor_name, notes)

    cursor.execute(insert_appointment_query, appointment_data)
    db.commit()
    print("Appointment record inserted successfully.")


def fetch_all_appointments(db):
    """Fetch all records from the 'appointments' table."""
    cursor = db.cursor()

    # Select the database
    cursor.execute("USE userdb")

    # Fetch all appointments
    select_appointments_query = """
    SELECT id, patient_id, DATE_FORMAT(appointment_date, '%Y-%m-%d') AS appointment_date, 
           appointment_time, doctor_name, notes
    FROM appointments
    """
    cursor.execute(select_appointments_query)
    appointments = cursor.fetchall()

    return appointments


def show_all_appointments(db):
    cursor = db.cursor()

    # Select the database
    cursor.execute("USE userdb")
    select_query = """
    SELECT id, patient_id, appointment_date, CAST(appointment_time AS CHAR), doctor_name, notes FROM appointments
    """
    cursor.execute(select_query)
    records = cursor.fetchall()

    if records:
        st.subheader("All Appointment Records")
        df = pd.DataFrame(records,
                          columns=['ID', 'Patient ID', 'Appointment Date', 'Appointment Time', 'Doctor Name', 'Notes'])
        st.dataframe(df)
    else:
        st.write("No appointments found")


def edit_booking_record(db, TsID, new_passenger_id,new_flight_id):
    """Edit an booking record in the 'appointments' table."""
    cursor = db.cursor()

   
    # Update the booking record
    update_booking_query = """
    UPDATE Transactions
    SET passenger = ?, Flight = ?
    WHERE TsID = ?
    """
    booking_data = (new_passenger_id,new_flight_id,TsID)

    cursor.execute(update_booking_query, booking_data)
    db.commit()


def fetch_booking_by_id(db, booking_id):
    """Fetch an appointment's record from the 'appointments' table based on ID."""
    cursor = db.cursor()


    # Fetch the appointment by ID
    select_booking_query = """
       SELECT TsID, BookingDate, DepartureDate, Passenger, Flight, Charges, Discount
        FROM Transactions
       WHERE TsID = ?
       """
    cursor.execute(select_booking_query, (booking_id,))
    booking = cursor.fetchone()
    #st.write(booking)
    return booking





def manage_booking(db):
    
    search_value = st.text_input("Enter Booking ID", key="search_value")

    if st.button("Search"):
        booking = fetch_booking_by_id(db, search_value)
        

        if booking:
            st.subheader("Appointment Details")
            df = pd.DataFrame([booking],
                              columns=['TsID', 'BookingDate', 'DepartureDate', 'Passenger', 'Flight', 'Charges', 'Discount'])
            st.dataframe(df)
            st.session_state.edit_booking = booking
        else:
            st.write("booking not found")
    if 'edit_booking' in st.session_state:
        edit_booking(db)


def edit_booking(db):
    # if 'edit_appointment' in st.session_state:
    booking = st.session_state.edit_booking
    st.subheader("Edit booking Details")
    new_passenger_id = st.number_input("passenger id", value=booking[3])
    new_flight = st.text_input("flight id", value=booking[4])

    if st.button("Update booking"):
        edit_booking_record(db, booking[0], new_passenger_id,new_flight)
        st.write("booking record updated successfully.")
        del st.session_state.edit_booking

def filter_search_flights(db):
    """Filter search flights with multiple options."""
    st.subheader("Search Flights :airplane:")

    # Add multiple filter inputs
    flight_id = st.text_input("Flight ID", key="flight_id")
    flight_date = st.date_input("Flight Date", key="flight_date")
    aircraft = st.text_input("Aircraft (AcNumber)", key="aircraft")
    airport = st.text_input("Airport", key="airport")

    if st.button("Search Flights"):
        # Build the query dynamically based on the filters provided
        filters = []
        params = []

        if flight_id:
            filters.append("FlID = ?")
            params.append(flight_id)
        if flight_date:
            filters.append("DATE(FlightDate) = ?")
            params.append(flight_date.strftime('%Y-%m-%d'))  # Convert date to string
        if aircraft:
            filters.append("Aircraft = ?")
            params.append(aircraft)
        if airport:
            filters.append("Airport = ?")
            params.append(airport)

        # If no filters are provided, show a message
        if not filters:
            st.warning("Please provide at least one search filter.")
            return

        # Construct the SQL query
        query = """
        SELECT FlID, FlightDate, Departure, Arrival, Aircraft, Airport, Destination
        FROM Flight_Schedule f
        INNER JOIN AirFare a ON f.NetFare = a.AfID
        INNER JOIN Route r ON a.Route = r.RtID
        """
        if filters:
            query += " WHERE " + " AND ".join(filters)

        # Execute the query
        cursor = db.cursor()
        cursor.execute(query, tuple(params))
        flights = cursor.fetchall()

        return flights
     


def edit_flights(db):
    """Edit a flights record in the 'flight schedule' table."""

    st.subheader("Edit flights Details")
    new_name = st.text_input("Enter new flight date", value=st.session_state.edit_flights[1])
    new_age = st.number_input("Enter new departute time", value=st.session_state.edit_flights[2])
    new_contact = st.text_input("Enter new arrival time", value=st.session_state.edit_flights[3])
    new_email = st.text_input("Enter new aircraft", value=st.session_state.edit_flights[4])
    new_address = st.text_input("Enter new destination", value=st.session_state.edit_flights[5])

    if st.button("Update :roller_coaster:"):
        patient_id = st.session_state.edit_flights[0]
        update_patient_info(db, patient_id, new_name, new_age, new_contact, new_email, new_address)


def update_patient_info(db, patient_id, new_name, new_age, new_contact, new_email, new_address):
    """Update a patient's record in the 'patients' table."""
    cursor = db.cursor()

    # Select the database
    cursor.execute("USE userdb")

    # Update the patient record
    update_patient_query = """
    UPDATE patients
    SET name = %s, age = %s, contact_number = %s, email = %s, address = %s
    WHERE id = %s
    """
    patient_data = (new_name, new_age, new_contact, new_email, new_address, patient_id)

    cursor.execute(update_patient_query, patient_data)
    db.commit()
    st.write("Patient record updated successfully.")

def generate_acnumber(db):
    cursor = db.cursor()
    
    # Query to get the maximum AcNumber
    cursor.execute("SELECT AcNumber FROM Aircrafts ORDER BY AcNumber DESC LIMIT 1")
    result = cursor.fetchone()
    
    if result is None:
        # If there are no records, start from AC001
        return "AC001"
    else:
        # Extract the numeric part of the AcNumber and increment it
        last_acnumber = result[0]
        numeric_part = int(last_acnumber[2:])  # Extract the number after "AC"
        new_numeric_part = numeric_part + 1
        return f"AC{new_numeric_part:03d}"  # Format with 3 digits, e.g., AC001, AC002

def generate_transactionID(db):
    cursor = db.cursor()
    cursor.execute("SELECT TsID FROM Transactions ORDER BY TsID DESC LIMIT 1")
    result = cursor.fetchone()
    
    if result is None:
        # If there are no records, start from AC001
        return 1
    else:
        # Extract the numeric part of the AcNumber and increment it
        return result[0]+1


def book_flights(db):
    cursor=db.cursor()
    st.subheader("Search Flights by date :airplane:")

    # Add multiple filter inputs
    flight_date = st.date_input("Flight Date", key="flight_date")
    from_location = st.text_input("from", key="from")
    to_location = st.text_input("to", key="to")

    if st.button("Search Flights"):
        # Build the query dynamically based on the filters provided
        filters = []
        params = []

        if flight_date:
            filters.append("DATE(FlightDate) = ?")
            params.append(flight_date.strftime('%Y-%m-%d'))  # Convert date to string
        if from_location:
            filters.append("Airport = ?")
            params.append(from_location)
        if to_location:
            filters.append("Destination = ?")
            params.append(to_location)

        # If no filters are provided, show a message
        if not filters:
            st.warning("Please provide at least one search filter.")
            return

        # Construct the SQL query
        query = """
        SELECT FlID, FlightDate, Departure, Arrival, Aircraft, Airport, Destination
        FROM Flight_Schedule f
        INNER JOIN AirFare a ON f.NetFare = a.AfID
        INNER JOIN Route r ON a.Route = r.RtID
        """
        if filters:
            query += " WHERE " + " AND ".join(filters)

        # Execute the query
        cursor = db.cursor()
        cursor.execute(query, tuple(params))
        flights = cursor.fetchall()
        st.session_state.flights=flights
        return flights
        
        


def book_flight_tickets(db):
    cursor=db.cursor()
    
    st.subheader('Enter booking details')
    components.html(htmlComponents.book_flights, height=400)
    #passengerid
    #booking date - today
    #flightid
    #type
    #employee -who booked the flight
    #charges
    #discount
    TsID = generate_transactionID(db)
    st.text_input("Booking ID (Auto-Generated)", value=TsID, disabled=True)
    
    #AcNumber = st.text_input("Enter aircraft number", key="AcNumber")
    
    passenger_id = st.number_input("Enter passenger id",value=1)
    flight_id = st.number_input("Enter Flight ID", step=1)
    
    flight_type=1
    employee=st.number_input('employee ID', value=1)
    charge_id=st.number_input('charge_id', value=20)
    discount=st.number_input('discount_id', value=15)
    
    if st.button("book ticket"):
            if not passenger_id or not flight_id :
                st.warning("Please fill all the necessary fields.")
            else:
                try:
                    # Insert new aircraft record
                    BookingDate=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    DepartureDate=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    for flight in st.session_state['flights']:
                        if flight[0] == flight_id:  # Assuming index 0 is FlID
                            DepartureDate = flight[2]  # Assuming index 1 is BookingDate
                            
                    insert_query = """
                    INSERT INTO Transactions (TsID, BookingDate, DepartureDate, Passenger,Flight,Type,Employee,Charges, Discount)
                        VALUES (?, ?, ?, ?,?,?,?,?,?)
                     """
                    #st.write(TsID,BookingDate,DepartureDate,passenger_id,flight_id,flight_type,employee,charge_id,discount)
                    cursor.execute(insert_query,(TsID,BookingDate,DepartureDate,passenger_id,flight_id,flight_type,employee,charge_id,discount))
                    db.commit()
                    # Fetch the auto-generated AcID
                    # new_acid = cursor.lastrowid
                    st.success(f"Successfully booked the ticket. booking confirmation ID: {TsID}")
                except sqlite3.IntegrityError as e:
                    st.error(f"An error occurred: {e}")
    
    
    




def main():
    # Title and sidebar
    st.title("Airlines Management System :airplane_arriving:")
    lott1 = loti("https://lottie.host/b262eef4-f923-48e5-9df9-9654b245381d/yTaASJbbWr.json")
    lotipatient = loti("https://lottie.host/1e57917a-e376-49d2-a274-613899e76a96/OVc4BfQMSn.json")
    db = create_connection()
    cursor = db.cursor()
    # create_database(db)

    # config['database'] = 'userdb'  # Update the database name
    # db = create_connection()

    # create_patients_table(db)
    # create_appointments_table(db)
    # modify_patients_table(db)

    menu = ["Home", "Add Flights/Schedule", "Show available flights", "book flights", "manage bookings"]
    options = st.sidebar.radio("Select an Option :dart:", menu)



    if options == "Home":
        st.subheader("Welcome to Airlines Management System:")
        st.write("Navigate from sidebar to access flight details and booking")
        st_lottie(lott1, height=800)
        # st.image('hospital.jpg', width=600)





    elif options == "Add Flights/Schedule":
        st.subheader("Enter Flight details 	:small_airplane::")
        st_lottie(lotipatient, height=200)
        # Automatically generate AcNumber
        AcNumber = generate_acnumber(db)
        st.text_input("Aircraft Number (Auto-Generated)", value=AcNumber, disabled=True)

        #AcNumber = st.text_input("Enter aircraft number", key="AcNumber")
        Capacity = st.number_input("Enter aircraft capacity", key="Capacity", value=150, min_value=5)
        MfdBy = st.text_input("aircraft manufactored by", key="MfdBy")
        MfdOn = st.text_input("Enter manufactored date(YYYY-MM-DD)", key="MfdOn")
        
        col1, col2,col3 =st.columns([1,3,1])
        with col1:
            if st.button("add aircraft record"):
                if not MfdBy or not MfdOn or not Capacity:
                    st.warning("Please fill all the fields.")
                else:
                    try:
                        # Insert new aircraft record
                        insert_query = """
                        INSERT INTO Aircrafts (AcNumber, Capacity, MfdBy, MfdOn)
                            VALUES (?, ?, ?, ?)
                        """
                        cursor.execute(insert_query,(AcNumber,Capacity,MfdBy,MfdOn))
                        db.commit()
                        # Fetch the auto-generated AcID
                        # new_acid = cursor.lastrowid
                        st.success(f"Aircraft record added successfully with AcNumber: {AcNumber}")
                    except sqlite3.IntegrityError as e:
                        st.error(f"An error occurred: {e}")
        with col3:
            if st.button("Schedule Flights"):
                schedule_new_flights(db)
                    



    elif options == "Show available flights":
        #flights = fetch_all_flights(db)
        flights = filter_search_flights(db)
        if flights:
            st.subheader("All available flights :magic_wand:")
            df = pd.DataFrame(flights,
                              columns=['FlID','FlightDate','Departure','Arrival','Aircraft','Airport', 'Destination'])
            st.dataframe(df)
        else:
            st.write("No flights found")
        
        

    
    elif options == "book flights":
        flights=book_flights(db)
        if flights:
            st.subheader("All available flights :magic_wand:")
            df = pd.DataFrame(flights,
                              columns=['FlID','FlightDate','Departure','Arrival','Aircraft','Airport', 'Destination'])
            st.dataframe(df)
            st.session_state.book_flights=flights
        else:
            st.write("No flights found")
        if 'book_flights' in st.session_state:
            book_flight_tickets(db)








    elif options == "manage bookings":
        manage_booking(db)
        flights=filter_search_bookings(db)
        # delete_option = st.selectbox("Select delete option", ["ID", "Name", "Contact Number"], key="delete_option")
        # delete_value = st.text_input("Enter delete value", key="delete_value")

        # if st.button("Delete"):
        #     delete_patient_record(db, delete_option, delete_value)

    elif options == "Add patients Appointments":
        patient_id = st.number_input("Enter patient ID:", key="appointment_patient_id")
        appointment_date = st.date_input("Enter appointment date:", key="appointment_date")
        appointment_time = st.time_input("Enter appointment time:", key="appointment_time")
        doctor_name = st.text_input("Enter doctor's name:", key="appointment_doctor_name")
        notes = st.text_area("Enter appointment notes:", key="appointment_notes")

        if st.button("Add Appointment"):
            insert_appointment_record(db, patient_id, appointment_date, appointment_time, doctor_name, notes)
            st.write("Appointment record added successfully.")

    elif options == "Show All Appointments":
        show_all_appointments(db)


    elif options == "Search and Edit Patients Appointments":

        search_appointment(db)

    db.close()


if __name__ == "__main__":
    main()