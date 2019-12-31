from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date, Time

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String(32))
    fullname = Column(String(32))
    nickname = Column(String(32))

    def __repr__(self):
        return "<User(name='%s', fullname='%s', nickname='%s')>" % (
                             self.name, self.fullname, self.nickname)


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
    __tablename__ = 'events'

    id = Column(Integer, primary_key=True)
    fullname = Column(String(32))
    car_brand = Column(String(32))
    car_number = Column(String(32))
    phone_number = Column(String(32))
    enter_date = Column(String(32))
    enter_time = Column(String(32))
    pre_payment = Column(Integer)
    token = Column(String(32))
    departure_date = Column(String(32))
    departure_time = Column(String(32))
    total_days = Column(Integer)
    after_payment = Column(Integer)
