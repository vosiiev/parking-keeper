from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date, Time, ForeignKey
from sqlalchemy.orm import relationship
from flask_login import UserMixin

Base = declarative_base()


class User(UserMixin, Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    username = Column(String(32))
    password = Column(String(256))
    role = Column(String(32))

    def __repr__(self):
        return "%d/%s/%s" % (self.id, self.username, self.password)



class Event(Base):
    '''
    Parking events info.
    Example:
    id: 1
    fullname: Петренко Олексій Іванович
    car_brand: Nissan
    car_number: АІ7208ВА
    phone_number: 0660280336
    enter_date: 21/12/2019 ???
    enter_time: 12:20
    pre_payment: 2000
    token:
    departure_date: 05/01/2020
    departure_time: 15:35
    total_days: 5
    after_payment: 2500

    '''
    __tablename__ = 'event'
    id = Column(Integer, primary_key=True)
    last_name = Column(String(32))
    first_name = Column(String(32))
    middle_name = Column(String(32))
    car_brand = Column(String(32))
    car_number = Column(String(32))
    phone_number = Column(String(32))
    enter_date = Column(Date)
    enter_time = Column(Time)
    pre_payment = Column(Integer)
    departure_date = Column(Date)
    departure_time = Column(Time)
    total_days = Column(Integer)
    after_payment = Column(Integer)


class Customer(Base):
    __tablename__ = 'customer'
    id = Column(Integer, primary_key=True)
    last_name = Column(String(32))
    first_name = Column(String(32))
    middle_name = Column(String(32))
    phone_number = Column(String(32))
    car = relationship('Car', backref='customer')


class Car(Base):
    __tablename__ = 'car'
    id = Column(Integer, primary_key=True)
    brand = Column(String(32))
    number = Column(String(32))
    customer_id = Column(Integer, ForeignKey('customer.id'))
