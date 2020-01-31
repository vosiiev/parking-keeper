from app import engine, db_session
from data import Base, User, Customer, Lot, Duty, Event, Car, Damage
#
# customer = db_session.query(Customer).get(3)
# print(customer.cars[0].brand)
#

#
event = db_session.query(Event).get(27)
events = db_session.query(Event).all()
# print(event.damage[0].hood)

#
# for item in event.damage:
#     print(item)
#
# print(event.damage[0].roof)
#
# for i in events[-1].damage:
#     print(i)

damage = db_session.query(Damage).all()

print(damage[0].event)
