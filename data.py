from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date, Time, ForeignKey, Boolean, Table, DateTime
from sqlalchemy.orm import relationship
from flask_login import UserMixin

Base = declarative_base()


onduty = Table(
    'onduty', Base.metadata,
    Column('duty_id', Integer, ForeignKey('duty.id')),
    Column('user_id', Integer, ForeignKey('user.id')),
    )


class User(UserMixin, Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    username = Column(String(32))
    password = Column(String(256))
    role = Column(String(32))
    last_name = Column(String(32))
    first_name = Column(String(32))
    middle_name = Column(String(32))
    duty = relationship('Duty', secondary=onduty, backref='users_on_duty')

    def __repr__(self):
        return "%d/%s/%s" % (self.id, self.username, self.password)


class Duty(Base):
    __tablename__ = 'duty'
    id = Column(Integer, primary_key=True)
    opened = Column(Boolean)
    num_free_lots = Column(Integer)
    num_cars_to_go = Column(Integer)
    additional_payment = Column(Integer)
    returned_payment = Column(Integer)
    datetime_opened = Column(DateTime)
    datetime_closed = Column(DateTime)


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
    token = Column(Integer)
    form_avail = Column(Boolean)
    closed = Column(Boolean)

    customer_id = Column(Integer, ForeignKey('customer.id'))
    lot_id = Column(Integer, ForeignKey('lot.id'))

    damage = relationship('Damage', backref='event')




class Customer(Base):
    __tablename__ = 'customer'
    id = Column(Integer, primary_key=True)
    last_name = Column(String(32))
    first_name = Column(String(32))
    middle_name = Column(String(32))
    phone_number = Column(String(32))
    cars = relationship('Car', backref='customer')
    event = relationship('Event', backref='customer')


class Car(Base):
    __tablename__ = 'car'
    id = Column(Integer, primary_key=True)
    brand = Column(String(32))
    number = Column(String(32))
    customer_id = Column(Integer, ForeignKey('customer.id'))


class Lot(Base):
    __tablename__ = 'lot'
    id = Column(Integer, primary_key=True)
    name = Column(String(32))
    price = Column(Integer)
    num_left = Column(Integer)
    event = relationship('Event', backref='lot')


class Damage(Base):
    __tablename__ = 'damage'
    id = Column(Integer, primary_key=True)
    head_lights = Column(Boolean)
    tail_lights = Column(Boolean)
    front_bumper = Column(Boolean)
    rear_bumber = Column(Boolean)
    hood = Column(Boolean)
    trunk = Column(Boolean)
    roof = Column(Boolean)
    left_front_wheel = Column(Boolean)
    right_front_wheel = Column(Boolean)
    left_rear_wheel = Column(Boolean)
    right_rear_wheel = Column(Boolean)
    left_front_wing = Column(Boolean)
    right_front_wing = Column(Boolean)
    left_rear_wing = Column(Boolean)
    right_rear_wing = Column(Boolean)
    middle_front_glass = Column(Boolean)
    middle_rear_glass = Column(Boolean)
    left_front_glass = Column(Boolean)
    left_rear_glass = Column(Boolean)
    right_front_glass = Column(Boolean)
    right_rear_glass = Column(Boolean)
    left_front_door = Column(Boolean)
    left_rear_door = Column(Boolean)
    right_front_door = Column(Boolean)
    right_rear_door = Column(Boolean)

    event_id = Column(Integer, ForeignKey('event.id'))
