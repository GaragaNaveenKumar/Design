
#Airline Management System
from abc import ABC, abstractmethod
from enum import Enum

class BookingStatus(Enum):
    IN_PROGRESS = "IN_PROGRESS"
    BOOKED = "BOOKED"
    CANCELLED = "CANCELLED"

class Seat(ABC):
    def __init__(self):
        self.is_occupied = False
    
    def occupy(self):
        self.is_occupied = True
    
    def release(self):
        self.is_occupied = False

class EconomySeat(Seat):

    def __init__(self, price):
        super().__init__()
        self.price = price
        self.bags_allowed = 1

class BusinessSeat(Seat):

    def __init__(self, price):
        super().__init__()
        self.price = price
        self.bags_allowed = 2

class Aircraft:

    def __init__(self, aircraft_number):
        self.aircraft_number = aircraft_number
        self.seats = {}
    
    def add_seats(self, seat: Seat, seat_number):
        self.seats[seat_number] = seat

class Flight:

    def __init__(self, flight_number,aircraft: Aircraft, source, destination, source_time, dest_time):
        self.flight_number = flight_number
        self.aircraft = aircraft
        self.source = source
        self.destination = destination
        self.source_time = source_time
        self.dest_time = dest_time
    
class Passenger:

    def __init__(self, email, name):
        self.email = email
        self.name = name

class Baggage(ABC):

    @abstractmethod
    def get_price(self):
        pass

class NormalBaggage(Baggage):

    def __init__(self, price) -> None:
        self.price = price
    
    def get_price(self):
        return self.price
    
class PaymentStrategy(ABC):
    @abstractmethod
    def process_payment(self, amount: float) -> bool:
        pass

class CreditCardPayment(PaymentStrategy):
    def __init__(self, card_number: str, cvv: str, expiry_date: str):
        self.card_number = card_number
        self.cvv = cvv
        self.expiry_date = expiry_date
    
    def process_payment(self, amount: float) -> bool:
        print(f"Processing credit card payment of ${amount:.2f}")
        return True

class PayPalPayment(PaymentStrategy):
    def __init__(self, email: str, password: str):
        self.email = email
        self.password = password
    
    def process_payment(self, amount: float) -> bool:
        print(f"Processing PayPal payment of ${amount:.2f}")
        return True

class Booking:

    def __init__(self, booking_id, passenger, flight):
        self.booking_id = booking_id
        self.passenger = passenger
        self.flight = flight
        self.bags = []
        self.seat = None
        self.booking_status = BookingStatus.IN_PROGRESS
    
    def select_seat(self, seat_number):
        selected_seat = self.flight.aircraft.seats[seat_number]
        if selected_seat.is_occupied:
            raise ValueError(f"Seat {seat_number} is already occupied")
        # If the passenger already had a seat, release it
        if self.seat:
            self.seat.release()
        self.seat = selected_seat
        self.seat.occupy()
        return True

    def add_baggage(self, bag: Baggage):
        self.bags.append(bag)
    
    def calculate_total_cost(self):
        cost = 0
        allowed_bags = self.seat.bags_allowed

        for bag in range(allowed_bags, len(self.bags)): #Skip the first n bags that are free with the seat
            cost += bag.get_price()
        
        cost += self.seat.price

        return cost
    
    def make_payment(self, payment_stratgey: PaymentStrategy):
        cost = self.calculate_total_cost()
        if payment_stratgey.process_payment(cost):
            self.booking_status = BookingStatus.BOOKED
        return True

class BookingManager:

    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(BookingManager, cls).__new__(cls)
            cls._instance.bookings = {}
            cls._instance.aircrafts = {}
            cls._instance.passengers = {}
            cls._instance.flights = {}
        return cls._instance

    def add_aircraft(self, aircraft: Aircraft):
        self.aircrafts[aircraft.aircraft_number] = aircraft
    
    def add_passenger(self, passenger: Passenger):
        self.passengers[passenger.email] = passenger
    
    def add_flight(self, flight: Passenger):
        self.flights[flight.flight_number] = flight

    def create_booking(self, passenger_email, flight_number):
        passenger = self.passengers[passenger_email]
        flight = self.flights[flight_number]
        booking_id = "some id"
        booking = Booking("some id", passenger, flight)
        self.bookings[booking_id] = booking
    
    def select_seat(self, booking_id, seat_number):
        booking = self.bookings[booking_id]
        booking.select_seat(seat_number)
    
    def add_bag(self, booking_id, bag: Baggage):
        booking = self.bookings[booking_id]
        booking.add_baggage(bag)
    
    def make_payment(self, booking_id, payment_stratgey: PaymentStrategy):
        booking = self.bookings[booking_id]
        booking.make_payment(payment_stratgey)
    
    def search_flights(self, source=None, destination=None, date=None):
        results = []

        if source is None and destination is None and date is None:
            return list(self.flights.values())
        
        for flight in self.flights.values():
            matches = True

            if source is not None:
                if flight.source.lower() != source.lower(): matches = False
            
            if destination is not None and matches:
                if flight.destination.lower() != destination.lower(): matches = False
            
            if date is not None and matches:
                flight_date = flight.source_time.split()[0]
                if flight_date != date: matches = False
        
            if matches:
                results.append(flight)
        
        return results