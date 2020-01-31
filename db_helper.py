from app import engine, db_session
from data import Base, User, Customer, Lot, Duty, Event, Car, Damage
from security import hash_password

u = User(username='admin', password=hash_password('admin'), role='admin')

db_session.add(u)
db_session.commit()
# d = Duty(opened=False)
# u = User(username='user1', password=hash_password('user1'), role='user')
# db_session.add(u)
# db_session.add(d)
# db_session.commit()
# d.users.append(u)
# db_session.commit()
