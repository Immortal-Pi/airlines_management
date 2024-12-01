import streamlit as st
import htmlComponents
import streamlit.components.v1 as components
from datetime import datetime
import sqlite3

@st.dialog('Schedule')
def schedule_new_flights(db):
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
                    st.success(f"Successfully scheduled the flight {aircraft_id}, confirmation ID: {flight_id}")
                except sqlite3.IntegrityError as e:
                    st.error(f"An error occurred: {e}")

