from app import engine, db_session
from data import Base, User, Customer, Lot, Duty, Event, Car, Damage
from security import hash_password
from datetime import datetime
import random

# last_names = [
#     'Шевченко',
#     'Мельник',
#     'Бондаренко',
#     'Коваль',
#     'Кравець',
#     'Коваленко',
#     'Кравченко',
#     'Ткаченко',
#     'Олійник',
#     'Бойко',
#     'Іванов',
#     'Хоменко',
#     'Чорний',
#     'Шаповал',
#     'Шевчук',
#     'Якименко',
#     'Яковенко',
#     'Антонюк',
#     'Вакуленко',
#     'Вовк',
# ]
#
# first_names = [
#     'Василь',
#     'Олег',
#     'Ігор',
#     'Євген',
#     'Степан',
#     'Петро',
#     'Віктор',
#     'Богдан',
#     'Сергій',
#     'Олександр',
#     'Григорій',
#     'Георгій',
#     'Святослав',
#     'Вячеслав',
#     'Микита',
#     'Дмитро',
#     'Андрій',
#     'Владислав',
#     'Олексій',
#     'Ілля',
# ]
#
# middle_names = [
#     'Григорович',
#     'Федорович',
#     'Андрійович',
#     'Анатолійович',
#     'Семенович',
#     'Олексійович',
#     'Васильович',
#     'Степанович',
#     'Олегович',
#     'Петрович',
#     'Віталійович',
#     'Володимирович',
#     'Ілліч',
#     'Миколайович',
#     'Євгенович',
#     'Юрійович',
#     'Іванович',
#     'Михайлович',
#     'Олегович',
#     'Сергійович',
#     'Ярославович',
# ]
#
# car_brands = [
#     'Nissan',
#     'Porsche',
#     'Ferrari',
#     'Daewoo',
#     'Ford',
#     'Chevrolet',
#     'Toyota',
#     'Honda',
#     'Yamaha',
#     'Mercedes',
#     'Suzuki',
#     'Peugeot',
#     'VAZ',
#     'Mitsubishi',
#     'Ferrari',
#     'Pagani',
#     'Chevrolet',
#     'Toyota',
#     'Honda',
#     'Yamaha',
# ]
#
#
# car_numbers = [
#     'AI3828II',
#     'BE2437CK',
#     'AX2100IA',
#     'AE5940MC',
#     'AM9473CX',
#     'AX1448AP',
#     'CA8001AP',
#     'CB0954CC',
#     'BT3615BC',
#     'CA0646IE',
#     'BI7170EE',
#     'AB3959EM',
#     'AA5371OO',
#     'AC9818AP',
#     'BX4752CX',
#     'AP7586HC',
#     'BH2770KB',
#     'BX0681CX',
#     'AT1495AI',
#     'AE3924ME',
#
#
# ]
#
#
# for i in range(20):
#     customer = Customer(
#         last_name=last_names[i],
#         first_name=first_names[i],
#         middle_name=middle_names[i],
#         phone_number=''.join(('+380', str(random.randint(1000000000,9999999999)))),
#     )
#
#     car = Car(
#         brand=car_brands[i],
#         number=car_numbers[i],
#         customer=customer,
#     )
#     db_session.add(customer)
#     db_session.add(car)
#
# db_session.commit()

customers = db_session.query(Customer).all()
for customer in customers:
    for car in customer.cars:
        print(car.number)
