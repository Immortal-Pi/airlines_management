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
from manage_passengers import manage_passengers
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

def fetch_all_flights(db):
    """Fetch all records from the 'Flight_Schedule' table."""
    cursor = db.cursor()

    # Fetch all flights schedule
    select_flight_query = "SELECT FlID,FlightDate,Departure,Arrival,Aircraft,Airport, Destination FROM Flight_Schedule f inner join AirFare a on f.NetFare=a.AfID inner join Route r on a.Route=r.RtID"
    cursor.execute(select_flight_query)
    flights = cursor.fetchall()
    return flights


def edit_booking_record(db, TsID, new_passenger_id,new_flight_id,new_charges,new_discount,cancel=False):
    """Edit an booking record in the 'Transaction' table."""
    cursor = db.cursor()

    if cancel:
        cancel_booking_query=""" 
            UPDATE Transactions
            SET Type = ?
                WHERE TsID = ?
        """
        cancel_data=(0,TsID)
        cursor.execute(cancel_booking_query, cancel_data)
        db.commit()
        #st.write(f'booking id : {TsID} cancelled')
    else:    
        # Update the booking record
        update_booking_query = """
        UPDATE Transactions
        SET passenger = ?, Flight = ?, Charges=?, Discount=?, Type=?
        WHERE TsID = ?
        """
        booking_data = (new_passenger_id,new_flight_id,new_charges,new_discount,1,TsID)

        cursor.execute(update_booking_query, booking_data)
        db.commit()


def fetch_booking_by_id(db, booking_id):
    """Fetch an appointment's record from the 'appointments' table based on ID."""
    cursor = db.cursor()


    # Fetch the appointment by ID
    select_booking_query = """
       SELECT TsID, BookingDate, DepartureDate, Passenger, Flight, Charges, Discount
        FROM Transactions
       WHERE TsID = ? and Type=?
       """
    cursor.execute(select_booking_query, (booking_id,1))
    booking = cursor.fetchone()
    #st.write(booking)
    return booking





def manage_booking(db):
    components.html(htmlComponents.modify_bookings, height=400)
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
    new_flight = st.number_input("flight id", value=booking[4])
    new_charges=st.number_input('Charges',value=booking[5])
    new_discount=st.number_input('Discount ID',value=booking[6])
    col1, col2,col3 =st.columns([1,2,1])
    with col1:
        if st.button("Update booking"):
                edit_booking_record(db, booking[0], new_passenger_id,new_flight,new_charges,new_discount)
                st.write(f"booking id: {booking[0]} updated successfully.")
                
    with col3:
        if st.button("cancel booking"):
                edit_booking_record(db, booking[0], new_passenger_id,new_flight,new_charges,new_discount,True)
                st.write(f"booking id: {booking[0]} cancelled successfully.")
                
    #del st.session_state.edit_booking

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
    components.html(htmlComponents.book_flights_2, height=400)
    
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
    book_flights_logo=loti('https://lottie.host/b16a24fd-d113-40e2-9d98-b5aaad1ad754/vCPSzBwWp1.json')
    db = create_connection()
    cursor = db.cursor()
    # create_database(db)

    # config['database'] = 'userdb'  # Update the database name
    # db = create_connection()

    # create_patients_table(db)
    # create_appointments_table(db)
    # modify_patients_table(db)

    menu = ["Home", "Add Flights/Schedule", "Show available flights","manage passenger", "book flights", "manage bookings"]
    options = st.sidebar.radio("Select an Option :dart:", menu)



    if options == "Home":
        #st.subheader("Welcome to Airlines Management System:")
        st.write("Navigate from sidebar to access flight details/booking and passenger details")
        st_lottie(lott1, height=800)
        # st.image('hospital.jpg', width=600)





    elif options == "Add Flights/Schedule":
        st.subheader("Enter Flight details 	:small_airplane::")
        #st_lottie(lotipatient, height=200)
        st.image('./assets/add_planes.png',width=400)
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
        st_lottie(book_flights_logo,height=300)
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
        #flights=filter_search_bookings(db)
        # delete_option = st.selectbox("Select delete option", ["ID", "Name", "Contact Number"], key="delete_option")
        # delete_value = st.text_input("Enter delete value", key="delete_value")

        # if st.button("Delete"):
        #     delete_patient_record(db, delete_option, delete_value)

    elif options == "manage passenger":
        st.subheader('Manage Passengers')
        st.image('./assets/passengers.png',width=600)
        manage_passengers(db)

    elif options == "Show All Appointments":
        manage_passengers(db)


    

    db.close()


if __name__ == "__main__":
    main()