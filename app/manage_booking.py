import streamlit as st
import htmlComponents
import streamlit.components.v1 as components
from datetime import datetime
import sqlite3
import pandas as pd

def filter_search_bookings(db):
    """Filter search flights with multiple options."""
    st.subheader("Search bookings 	:ledger:")
    components.html(htmlComponents.modify_bookings,height=400)
    # Add multiple filter inputs
    TsID = st.number_input("Booking ID", placeholder='1',step=1)
    booking_date = st.date_input("Flight Date")
    passenger_id = st.number_input("passneger ID", key="aircraft",step=1)
    flight_id = st.number_input("Airport", key="airport",step=1)
    employee_id = st.number_input('Enter Employee ID',step=1)
    
    if st.button("Search bookings"):
        # Build the query dynamically based on the filters provided
        filters = []
        params = []

        if TsID:
            filters.append("TsID = ?")
            params.append(TsID)
        if booking_date:
            filters.append("DATE(BookingDate) = ?")
            params.append(booking_date.strftime('%Y-%m-%d'))  # Convert date to string
        if passenger_id:
            filters.append("Passenger = ?")
            params.append(passenger_id)
        if flight_id:
            filters.append("Flight = ?")
            params.append(employee_id)
        if employee_id:
            filters.append("Employee = ?")
            params.append(employee_id)

        # If no filters are provided, show a message
        if not filters:
            st.warning("Please provide at least one search filter.")
            return

        # Construct the SQL query
        query = """
        SELECT TsID, BookingDate, DepartureDate, Passenger, Flight, Charges, Discount
        FROM Transactions 
        """
        if filters:
            query += " WHERE " + " AND ".join(filters)

        # Execute the query
        cursor = db.cursor()
        cursor.execute(query, tuple(params))
        flights = cursor.fetchall()
        
        
        if flights:
            st.subheader('Booking Details')
            
            st.dataframe(flights)
            st.session_state.edit_booking=flights
    
    
    if st.button('modify booking'):
        modify_booking()

@st.dialog('Edit booking')
def modify_booking():
    db=sqlite3.connect('setup/airlines.db')
    flights=st.session_state['edit_booking']
    cursor=db.cursor()
    st.subheader('Modify booking')
    components.html(htmlComponents.edit_flights, height=400)
    
    try:
        booking_id=st.number_input('Enter Booking ID' )
            
           
                
                    

    except:
        st.write('invalid booking ID')
        # appointment = st.session_state.edit_appointment
        # st.subheader("Edit Appointment Details")
        # new_appointment_date = st.date_input("Appointment Date", value=appointment[2])
        # new_appointment_time = st.text_input("Appointment Time", value=appointment[3])
        # new_doctor_name = st.text_input("Doctor Name", value=appointment[4])
        # new_notes = st.text_input("Notes", value=appointment[5])

    
        

        

@st.dialog('Schedule')
def cancel_booking(db):
    db=sqlite3.connect('setup/airlines.db')
    cursor=db.cursor()
    st.subheader('Schedule new Flights')
    components.html(htmlComponents.edit_flights, height=400)
    with st.form('Schedule flight'):
        flight_id=st.number_input('Flight ID', step=1)
        flight_date=st.date_input('Flight Date')
        departure_time=st.time_input('Departure time')
        arrival_date=st.date_input('Arrival Date',value=flight_date)
        arrival_time=st.time_input('Arrival time')
        aircraft_id=st.text_input('Aircraft ID', placeholder='AC001')
        net_fair=st.number_input('Fair ID', step=1)
        submit_button=st.form_submit_button('Submit')

        if submit_button:
            if not flight_id or not departure_time or not arrival_time or not aircraft_id or not net_fair :
                st.warning("Please fill all the necessary fields.")
                
                
            else:
                try:
                    # Insert new aircraft record
                    departure_time=datetime.strptime(f'{flight_date} {departure_time}', '%Y-%m-%d %H:%M:%S')
                    arrival_time=datetime.strptime(f'{arrival_date} {arrival_time}', '%Y-%m-%d %H:%M:%S')
                            
                    insert_query = """
                    INSERT INTO Flight_Schedule (FlID,FlightDate,Departure,Arrival,Aircraft,NetFare)
                        VALUES (?, ?, ?, ?,?,?)
                     """
                    #st.write(flight_id,departure_time,flight_date,departure_time,arrival_date,arrival_time,aircraft_id,net_fair)
                    cursor.execute(insert_query,(flight_id,departure_time,departure_time,arrival_time,aircraft_id,net_fair))
                    db.commit()
                    # Fetch the auto-generated AcID
                    # new_acid = cursor.lastrowid
                    st.success(f"Successfully booked the ticket. booking confirmation ID: {flight_id}")
                except sqlite3.IntegrityError as e:
                    st.error(f"An error occurred: {e}")