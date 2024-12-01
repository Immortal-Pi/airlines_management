import streamlit as st
import htmlComponents
import streamlit.components.v1 as components
from datetime import datetime
import sqlite3
import pandas as pd

def edit_passenger_record(db,psid,new_name,new_address,new_nationality,new_contact,delete=False):
     """Edit an passenger record in the 'Passenger' table."""
     cursor=db.cursor()
     if delete:
          delete_passenger_query = "DELETE FROM passengers WHERE PsID = ?"
          cursor.execute(delete_passenger_query, (psid,))
          db.commit()
     else:
          update_passenger_query=""" 
            update Passengers 
            set Name=?, Address=?, Nationality=?, Contacts=?
            where PsID=?
            """
          update_data=(new_name,new_address,new_nationality,new_contact,psid)
          cursor.execute(update_passenger_query, update_data)
          db.commit()
     

def edit_passenger(db):
    st.subheader('Edit Passenger Details')
    passenger=st.session_state.edit_passenger
    new_name=st.text_input("Name", value=passenger[1])
    new_address=st.text_input("Address", value=passenger[2])
    new_nationality=st.text_input("Nationality", value=passenger[4])
    new_contact=st.number_input("Contact", value=passenger[5])
    col1, col2,col3 =st.columns([1,3,1])
    with col1:
        if st.button("Update passenger"):
                edit_passenger_record(db, passenger[0],new_name,new_address,new_nationality,new_contact)
                st.write(f"passenger id: {passenger[0]}: {passenger[1]} updated successfully.")
                
    with col3:
        if st.button("delete passenger"):
                edit_passenger_record(db, passenger[0],new_name,new_address,new_nationality,new_contact,True)
                st.write(f"passenger id: {passenger[0]}: {passenger[1]} deleted successfully.")
                del st.session_state.edit_passenger
                


def fetch_passenger_by_id(db,passenger_id):
    """ Fetch Passenger record by id"""
    cursor=db.cursor()

    get_passenger_query=""" 
    select PsID,Name,Address,Age,Nationality,Contacts from Passengers where PsID=?
    """
    cursor.execute(get_passenger_query,(passenger_id,))
    passengers=cursor.fetchone()
    return passengers

def manage_passengers(db):
    
    passenger_id=st.number_input('Enter Passenger ID',step=1, value=10) 
    if st.button('Search'):
        passenger=fetch_passenger_by_id(db,passenger_id)
        #st.write(passenger)
        if passenger:
            st.subheader('Passenger Details')
            #st.write(passenger)
            st.session_state.edit_passenger=passenger
        else:
            st.write('passenger ID not found')
            if 'edit_passenger' in st.session_state:
                del st.session_state.edit_passenger
    if 'edit_passenger' in st.session_state:
        edit_passenger(db)
        #del st.session_state.edit_passenger

    if st.button('Add Passenger'):
         add_passenger(db) 

@st.dialog('Add Passenger Details')         
def add_passenger(db):
    db=sqlite3.connect('setup/airlines.db')
    cursor=db.cursor()
    #st.subheader('Schedule new Flights')
    passenger_id=generate_passengerID(db)
    components.html(htmlComponents.edit_flights, height=400)
    with st.form('Schedule flight'):
        
        psID=st.number_input('Passenger ID (Auto Generated)',value=passenger_id,disabled=True)
        Name=st.text_input('Name')
        Address=st.text_input('Addresss')
        Age=st.number_input('Age',placeholder='Years',step=1)
        Nationality=st.text_input('Nationality')
        Contact_No=st.number_input('Contact Nubmer', placeholder='XXXXXXXXXX',step=1)
        submit_button=st.form_submit_button('Submit')

        if submit_button:
            if not Name or not Address or not Age or not Nationality or not Contact_No:
                st.warning("Please fill all the necessary fields.")
                
                
            else:
                try:
                    
                            
                    insert_query = """
                    INSERT INTO Passengers (PsID,Name,Address,Age,Nationality,Contacts)
                        VALUES (?, ?, ?, ?,?,?)
                     """
                    #st.write(flight_id,departure_time,flight_date,departure_time,arrival_date,arrival_time,aircraft_id,net_fair)
                    cursor.execute(insert_query,(psID,Name,Address,Age,Nationality,Contact_No))
                    db.commit()
                    # Fetch the auto-generated AcID
                    # new_acid = cursor.lastrowid
                    st.success(f"Successfully added passenger {Name} with ID: {psID}")
                except sqlite3.IntegrityError as e:
                    st.error(f"An error occurred: {e}")

def generate_passengerID(db):
    cursor = db.cursor()
    cursor.execute("SELECT PsID FROM Passengers ORDER BY PsID DESC LIMIT 1")
    result = cursor.fetchone()
    
    if result is None:
        # If there are no records, start from AC001
        return 1
    else:
        # Extract the numeric part of the AcNumber and increment it
        return result[0]+1