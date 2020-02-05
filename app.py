from sqlalchemy import create_engine
from flask import Flask, Response, render_template, request, redirect, \
                    session, url_for, escape, abort
from sqlalchemy.orm import sessionmaker
from model import Event, User, Customer, Car, Duty, Lot, Damage
from flask_login import LoginManager, login_required, \
                        login_user, logout_user, current_user
from security import hash_password, verify_password
import logging
from functools import wraps
from datetime import datetime, date, time, timedelta

app = Flask(__name__)
app.secret_key = b'\xec\x18\xd6\x08y\xcb\xa2\r^\xdb\xc4\xf9U\x0fj"'
engine = create_engine('mysql+mysqlconnector://p_user:R3cogn1se!@localhost/parking', echo=True)
Session = sessionmaker(bind=engine)
db_session = Session()
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"
logging.basicConfig(filename='info.log',level=logging.DEBUG)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        for user in db_session.query(User).all():
            if username == user.username:
                if verify_password(user.password, password):
                    login_user(user)
                    logging.info(f'{user.username} logged in')
                    return redirect(url_for('journal'))
                else:
                    error = 'Невірно введений пароль'
                    logging.info(f'{user.username} failed to log in')
                    return render_template('login.html', error=error)
        else:
            error = 'Користувача з таким іменем не знайдено'
            logging.info(f'{username} doesn\'t exist')
            return render_template('login.html', error=error)
    else:
        return render_template('login.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/')


@login_manager.user_loader
def load_user(user_id):
    return db_session.query(User).filter_by(id=user_id).one()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/journal', methods=['GET', 'POST'])
@login_required
def journal():
    '''
    If POST: get data from journal page form
    and save it to database.
    If GET: retrieve data from database and render the journal page.

    Lot types:
    1. Відкрита зона (2.5х5)
    2. Відкрита зона (>5)
    3. Відкрита зона (парне одне місце)
    4. Відкрита зона (парне два місця)
    5. Бокс
    6. Бокс (парний одне місце)
    7. Бокс (парний два місця)
    8. Навіс
    '''
    if request.method == 'POST':
        try:
            customer_id = int(request.form['customer_id'])
            car_number = request.form['car_number']
            num_days = int(request.form['num_days'])
            token = int(request.form['token'])
            lot_type = int(request.form['lot_type'])
        except ValueError as e:
            return render_template('login.html', error=e)

        # Get customer and car data to auto create event.
        customer = db_session.query(Customer).filter_by(id=customer_id).one()
        try:
            car = db_session.query(Car).filter_by(number=car_number, customer=customer).one()
        except:
            error = 'У даного клієнта немає такого авто'
            return render_template('journal.html', error=error)

        pre_payment = calculate_payment(lot_type, num_days)

        # Check which lot is taken and get it from db.
        combine_lot_type = 0
        if lot_type == 7:
            combine_lot_type = 3
        elif lot_type == 8:
            combine_lot_type = 5
        else:
            combine_lot_type = lot_type
        lot = db_session.query(Lot).filter_by(id=combine_lot_type).one()

        # Work with lot types that can contain either 1 or 2 cars.
        takes_both_places = False
        if lot_type == 7 or lot_type == 8:
            lot.num_left -= 2
            takes_both_places = True
        else:
            lot.num_left -= 1

        try:
            new_event = Event(
                last_name=customer.last_name,
                first_name=customer.first_name,
                middle_name=customer.middle_name,
                car_brand=car.brand,
                car_number=car.number,
                phone_number=customer.phone_number,
                token=token,
                enter_datetime=datetime.now(),
                pre_payment=pre_payment,
                takes_both_places=takes_both_places,
                lot=lot,
                customer=customer,
                total_days=num_days,
                form_avail=False,
                closed=False,
            )
            # Get initial car damage from checkboxes (to avoid problems with clients)
            damage = Damage(
                head_lights=bool(request.form.getlist('head_lights')),
                tail_lights=bool(request.form.getlist('tail_lights')),
                front_bumper=bool(request.form.getlist("front_bumper")),
                rear_bumber=bool(request.form.getlist("rear_bumber")),
                hood=bool(request.form.getlist("hood")),
                trunk=bool(request.form.getlist("trunk")),
                roof=bool(request.form.getlist("roof")),
                left_front_wheel=bool(request.form.getlist("left_front_wheel")),
                right_front_wheel=bool(request.form.getlist("right_front_wheel")),
                left_rear_wheel=bool(request.form.getlist("left_rear_wheel")),
                right_rear_wheel=bool(request.form.getlist("right_rear_wheel")),
                left_front_wing=bool(request.form.getlist("left_front_wing")),
                right_front_wing=bool(request.form.getlist("right_front_wing")),
                left_rear_wing=bool(request.form.getlist("left_rear_wing")),
                right_rear_wing=bool(request.form.getlist("right_rear_wing")),
                middle_front_glass=bool(request.form.getlist("middle_front_glass")),
                middle_rear_glass=bool(request.form.getlist("middle_rear_glass")),
                left_front_glass=bool(request.form.getlist("left_front_glass")),
                left_rear_glass=bool(request.form.getlist("left_rear_glass")),
                right_front_glass=bool(request.form.getlist("right_front_glass")),
                right_rear_glass=bool(request.form.getlist("right_rear_glass")),
                left_front_door=bool(request.form.getlist("left_front_door")),
                left_rear_door=bool(request.form.getlist("left_rear_door")),
                right_front_door=bool(request.form.getlist("right_front_door")),
                right_rear_door=bool(request.form.getlist("right_rear_door")),
                event=new_event,
            )
            db_session.add(damage)
            db_session.add(new_event)
            db_session.commit()
        except Exception as e:
            return render_template('journal.html', error=e)
        return redirect(url_for('journal'))
    else:
        duties = db_session.query(Duty).all()
        duty = None
        if duties:
            duty = duties[-1]
        events = db_session.query(Event).all()
        damage = db_session.query(Damage).all()
        return render_template('journal.html', events=events, damage=damage,
                                                duty=duty)


def calculate_payment(lot_type, num_days):
    '''
    Calculates estimated lot price.
    '''
    if lot_type == 1:
        return 30*num_days
    elif lot_type == 2:
        return 50*num_days
    elif lot_type == 3:
        return 30*num_days
    elif lot_type == 7:
        return 60*num_days
    elif lot_type == 4:
        return 80*num_days
    elif lot_type == 5:
        return 80*num_days
    elif lot_type == 8:
        return 160*num_days
    elif lot_type == 6:
        return 60*num_days


@app.route('/customers', methods=['GET', 'POST'])
@login_required
def customers():
    '''
    'GET': show customers table.
    'POST': save a new customer or add a car to existing customer.
    '''
    if request.method == 'POST':
        fullname = (request.form['fullname']).split()
        last_name = fullname[0]
        first_name = fullname[1]
        if len(fullname) == 3:
            middle_name = fullname[2]
        else:
            middle_name = ''
        phone_number = request.form['phone_number']
        car_brand = request.form['car_brand']
        car_number = request.form['car_number']
        new_customer = Customer(
                last_name=last_name,
                first_name=first_name,
                middle_name=middle_name,
                phone_number=phone_number,
            )
        new_car = Car(
                brand=car_brand,
                number=car_number,
                customer=new_customer,
            )
        db_session.add(new_customer)
        db_session.add(new_car)
        db_session.commit()
        return redirect(url_for('customers'))
    else:
        customers = db_session.query(Customer).all()
        return render_template('customers.html', customers=customers)


@app.route('/journal/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_event(id):
    '''
    Retrieve data from journal event edit form and
    save it to the database. Accessible only to 'admin' user.
    '''
    event = db_session.query(Event).get(id)
    if request.method == 'POST':
        try:
            fullname = (request.form['fullname']).split()
            enter_date = request.form['enter_date']
            enter_time = request.form['enter_time']
            enter_datetime = ' '.join((enter_date, enter_time))
            event.last_name = fullname[0]
            event.first_name = fullname[1]
            event.middle_name = fullname[2]
            event.car_brand = request.form['car_brand']
            event.car_number = request.form['car_number']
            event.phone_number = request.form['phone_number']
            event.token = request.form['token']
            event.enter_datetime = datetime.strptime(enter_datetime, '%Y-%m-%d %H:%M')
            event.pre_payment = request.form['pre_payment']
            event.token = request.form['token']
            event.departure_date = request.form['departure_date']
            event.departure_time = request.form['departure_time']
            event.total_days = request.form['total_days']
            event.after_payment = request.form['after_payment']
        except Exception as e:
            return render_template('journal.html', error=e)
        db_session.commit()
        return redirect(url_for('journal'))
    else:
        return render_template('journal.html', edit_event=event)


@app.route('/journal/pre_close_event/<int:id>')
@login_required
def pre_close_event(id):
    '''
    Calculate final lot price and commit car's departure time.
    '''
    event = db_session.query(Event).get(id)

    delta = datetime.now() - event.enter_datetime
    delta_days = delta.days - event.total_days
    if event.takes_both_places:
        after_payment = event.lot.price * delta_days * 2
    else:
        after_payment = event.lot.price * delta_days

    event.departure_datetime = datetime.now()
    event.after_payment = after_payment
    db_session.commit()
    return redirect(url_for('journal'))


@app.route('/journal/close_event/<int:id>', methods=['POST'])
@login_required
def close_event(id):
    '''
    Save events data to duty's summary and ask if a customer took a car
    by himself/herself or the other person did it (if so, a physical
    affirmation paper needs to be filled).
    '''
    if request.method == 'POST':
        event = db_session.query(Event).get(id)
        delta = datetime.now() - event.enter_datetime
        delta_days = delta.days - event.total_days
        if event.takes_both_places:
            event.lot.num_left += 2
            after_payment = event.lot.price * delta_days * 2
        else:
            event.lot.num_left += 1
            after_payment = event.lot.price * delta_days

        event.form_avail = bool(request.form.getlist('form_avail'))
        event.departure_datetime = datetime.now()
        event.after_payment = after_payment
        event.closed = True
        db_session.commit()
        return redirect(url_for('journal'))


@app.route('/customers/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_customer(id):
    '''
    Retrieve data from customer edit form and
    save it to the database.
    '''
    customer = db_session.query(Customer).get(id)
    if request.method == 'POST':
        fullname = (request.form['fullname']).split()
        customer.last_name = fullname[0]
        customer.first_name = fullname[1]
        customer.middle_name = fullname[2]
        customer.phone_number = request.form['phone_number']
        for i in range(len(customer.cars)):
            customer.cars[i].brand = request.form[f'car_brand_{i}']
            customer.cars[i].number = request.form[f'car_number_{i}']
        db_session.commit()
        return redirect(url_for('customers'))
    else:
        return render_template('customers.html', edit_customer=customer)


@app.route('/customers/add_car/<int:id>', methods=['GET', 'POST'])
@login_required
def add_customer_car(id):
    '''
    Add car to a customer if he or she has more than 1 vehicle.
    '''

    if request.method == 'POST':
        brand = request.form['add_car_brand']
        number = request.form['add_car_number']
        customer=db_session.query(Customer).get(id)
        new_car = Car(
                brand=brand,
                number=number,
                customer=customer,
            )
        db_session.commit()
        return redirect(url_for('customers'))
    else:
        return render_template('customers.html')


@app.route('/journal/delete/<int:id>')
@login_required
def delete_event(id):
    '''
    Delete journal event on button click.
    '''
    event = db_session.query(Event).get(id)
    damage = db_session.query(Damage).filter_by(event_id=event.id).one()
    db_session.delete(event)
    db_session.delete(damage)
    db_session.commit()
    return redirect(url_for('journal'))


@app.route('/customers/delete/<int:id>')
@login_required
def delete_customer(id):
    '''
    Delete customer on button click.
    '''
    customer = db_session.query(Customer).get(id)
    cars = db_session.query(Car).filter_by(customer_id=customer.id)
    db_session.delete(customer)
    for car in cars:
        db_session.delete(car)
    db_session.commit()
    return redirect(url_for('customers'))


def find_duty_events(events, duty):
    '''
    Each duty starts about 8:00 and 20:00 (2 duties per day).
    Calculate events finishing on this duty (cars to depart).
    '''
    duty_events = []
    duty_end = datetime.now() + timedelta(hours=12)
    for event in events:
        departure_date = event.enter_datetime + timedelta(days=event.total_days)
        if (departure_date > duty.opened_datetime and
            departure_date < duty_end):
            duty_events.append(event)
    return duty_events


@app.route('/duty', methods=['GET', 'POST'])
@login_required
def duty():
    '''
    'GET': Receive duty's information (staff, number of free lots, number of
    cars to depart, open time).
    'POST': Open a new duty.
    '''
    if request.method == 'POST':
        duty = Duty(
            opened=True,
            num_cars_to_go=0,
            additional_payment=0,
            returned_payment=0,
            total_money=0,
            opened_datetime=datetime.now(),
        )

        worker_id = int(request.form['worker'])
        worker = db_session.query(User).get(worker_id)
        security_id = int(request.form['security'])
        security = db_session.query(User).get(security_id)

        duty.users.append(current_user)
        duty.users.append(worker)
        duty.users.append(security)
        db_session.add(duty)
        db_session.commit()
        return redirect(url_for('duty'))
    else:
        duties = db_session.query(Duty).all()
        events = db_session.query(Event).all()
        users = db_session.query(User).all()
        lots = db_session.query(Lot).all()

        now = datetime.now()
        if duties:
            duty = duties[-1]
        else:
            duty = Duty(
                opened=True,
                num_cars_to_go=0,
                additional_payment=0,
                returned_payment=0,
                total_money=0,
                opened_datetime=now,
            )

            duty.users.append(current_user)

        duty_events = find_duty_events(events, duty)
        logging.info(duty_events)
        # date_leave =  event.enter_datetime + timedelta(days=event.total_days)
        return render_template('duty.html', duty=duty, events=duty_events,
                                            lots=lots, users=users)


@app.route('/close_duty/<int:id>')
@login_required
def close_duty(id):
    '''
    Close duty and save info about events to db.
    '''
    duty = db_session.query(Duty).get(id)
    events = db_session.query(Event).all()
    for user in duty.users:
        if current_user == user or current_user.username == 'admin':
            duty.closed_datetime = datetime.now()
            duty.opened = False
            duty_events = find_duty_events(events, duty)

            for event in duty_events:
                if event.closed:
                    duty.total_money += event.after_payment
                    if event.after_payment > 0:
                        duty.additional_payment += event.after_payment
                    else:
                        duty.returned_payment += event.after_payment

            db_session.commit()
            return redirect(url_for('duty'))
        else:
            error = 'Закрити зміну може лише той, хто її відкрив'
            return render_template('duty.html', duty=duty, error=error)

    error = 'Невідома помилка'
    return render_template('duty.html', duty=duty, error=error)



if __name__ == '__main__':
    app.run(debug=True)
