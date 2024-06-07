# Copyright (c) Microsoft. All rights reserved.
# Licensed under the MIT license. See LICENSE file in the project root for full license information.

from datetime import date
import random
from pydantic import Field
import json

bookings = {
    "flights": [], 
    "accomodations": []   
}

emails = []


def send_booking_email(email: str, booking_details: dict) -> str:
    """Send an email with full booking details. The booking details must be a dictionary."""
    print(f"Sending email to {email}")
    email_booking = []
    value = {}
    if not isinstance(booking_details, dict ):
        value = booking_details.__dict__
    else:
        value = booking_details
    email_booking.append(value)
    
    message = f"Dear traveller, \n\nWe are happy to confirm your booking. Here are the details: \n\n{json.dumps(obj= value, indent=4)}\n\nHave a great trip!\n\nThe travel team"
    print(f"Email sent to {email} : { message}")
    emails.append(message)
    return f"Email sent to {email}"

def get_bookings() -> dict:
    """Usfeful for getting bookings."""
    return bookings

def find_flights(
        origin: str, 
        destination:str, 
        date: date
        ) -> list[dict]:
    """Can find flights on a specific date between a departure and destination."""
    values : list[dict] = []
    for i in range(random.randrange(3, 10)):
        values.append({
            "name": f"Flight {i}",
            "date": date,
            "origin": origin,
            "departure_time": f"{random.randrange(3, 19)}:00",
            "price_pp": f"€{random.randrange(100, 1000)}",
            "destination": destination
        })
    
    return values

def book_flight(
        flight_name: str, 
        origin: str,
        destination: str,
        departure_date: date, 
        passengers: int
        ) -> dict:
    """Can book a flight on a date for any number of passengers. It returns the booking confirmation."""
    flight_booking ={
        "name": flight_name,
        "date": departure_date,
        "passengers": passengers,
        "origin": origin,
        "destination": destination,
        "booking_reference": random.randrange(1000, 9999)
    }

    bookings["flights"].append(flight_booking)

    return flight_booking

def find_accomodations(
        location: str, 
        date: date
        ) -> list[dict]:
    """Can find accomodations for a given location and date."""
    values : list[dict] = []
    for i in range(random.randrange(3, 10)):
        values.append(
            {
                "name": f"Accomodation {i}",
                "location": location,
                "date": date,
                "price_pn": f"€{random.randrange(100, 333)}",
            }
        )
           
    
    return values

def book_accomodation(
        accomodation_name: str, 
        check_in_date: date, 
        nights:int, 
        guests: int
        ) -> dict:
    """Can book accomodation for a geoup of guests on specific date and number on nightrs. It returns the booking confirmation including the booking reference."""
    accomodation_booking = {
        "name": accomodation_name,
        "date": check_in_date,
        "nights": nights,
        "guests": guests,
        "booking_reference": random.randrange(1000, 9999)
    }

    bookings["accomodations"].append(accomodation_booking)

    return accomodation_booking