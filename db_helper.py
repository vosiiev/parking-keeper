from app import engine, db_session
from data import Base, User, Customer, Lot, Duty, Event, Car, Damage
from security import hash_password
from datetime import datetime

now = datetime.now()
date_opened = now.strftime('%Y-%m-%d')
time_opened = now.strftime('%H:%M:%S')

print(date_opened + ' ' + time_opened)

a = datetime.strptime(date_opened, '%Y-%m-%d')

print(type(date_opened))
print(type(a))
print(now.time())
# u = User(username='user1', password=hash_password('user1'), role='user')
# db_session.add(u)
# db_session.add(d)
# db_session.commit()
# d.users.append(u)
# db_session.commit()

# lots = db_session.query(Lot).all()
# for lot in lots:
#     print(lot.num_left)
