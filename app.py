from sqlalchemy import create_engine
from flask import Flask, Response, render_template, request, redirect, \
                    session, url_for, escape, abort
from sqlalchemy.orm import sessionmaker
from data import Event, User, Customer, Car
from flask_login import LoginManager, login_required, \
                        login_user, logout_user, current_user
from security import hash_password, verify_password
import logging
from functools import wraps
from datetime import datetime, date, time

app = Flask(__name__)
app.secret_key = b'\xec\x18\xd6\x08y\xcb\xa2\r^\xdb\xc4\xf9U\x0fj"'
engine = create_engine('mysql+mysqlconnector://p_user:R3cogn1se!@localhost/parking', echo=True)
Session = sessionmaker(bind=engine)
db_session = Session()
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"
logging.basicConfig(filename='info.log',level=logging.DEBUG)


@app.route('/login', methods=["GET", "POST"])
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
        # fullname = (request.form['fullname']).split()
        # last_name = fullname[0]
        # first_name = fullname[1]
        # middle_name = fullname[2]
        # car_brand = request.form['car_brand']
        # car_number = request.form['car_number']
        # phone_number = request.form['phone_number']
        # token = request.form['token']
        # enter_date = datetime.strptime(request.form['enter_date'], '%Y-%m-%d')
        # enter_time = datetime.strptime(request.form['enter_time'], '%H:%M')
        # pre_payment = request.form['pre_payment']
        # departure_date = datetime.strptime(request.form['departure_date'], '%Y-%m-%d')
        # departure_time = datetime.strptime(request.form['departure_time'], '%H:%M')
        # total_days = request.form['total_days']
        # after_payment = request.form['after_payment']
        try:
            customer_id = int(request.form['customer_id'])
            car_number = request.form['car_number']
            num_days = int(request.form['num_days'])
            token = int(request.form['token'])
            lot_type = int(request.form['lot_type'])
        except ValueError as e:
            return render_template('login.html', error=e)

        customer = db_session.query(Customer).filter_by(id=customer_id).one()
        car = db_session.query(Car).filter_by(number=car_number).one()

        now = datetime.now()
        enter_date = now.strftime('%Y-%m-%d')
        enter_time = now.strftime('%H:%M:%S')

        pre_payment = calculate_payment(lot_type, num_days)

        try:
            new_event = Event(
                    last_name=customer.last_name,
                    first_name=customer.first_name,
                    middle_name=customer.middle_name,
                    car_brand=car.brand,
                    car_number=car.number,
                    phone_number=customer.phone_number,
                    token=token,
                    enter_date=enter_date,
                    enter_time=enter_time,
                    pre_payment=pre_payment,
                    lot_type=lot_type,
                    # departure_date=departure_date.date(),
                    # departure_time=departure_time.time(),
                    # total_days=total_days,
                    # after_payment=after_payment,
                )
            db_session.add(new_event)
            db_session.commit()
        except Exception as e:
            return render_template('journal.html', error=e)
        return redirect(url_for('journal'))
    else:
        events = db_session.query(Event).all()
        return render_template('journal.html', events=events)


def calculate_payment(lot_type, num_days):
    if lot_type == 1:
        return 30*num_days
    elif lot_type == 2:
        return 50*num_days
    elif lot_type == 3:
        return 30*num_days
    elif lot_type == 4:
        return 60*num_days
    elif lot_type == 5:
        return 80*num_days
    elif lot_type == 6:
        return 80*num_days
    elif lot_type == 7:
        return 160*num_days
    elif lot_type == 8:
        return 60*num_days


@app.route('/customers', methods=['GET', 'POST'])
@login_required
def customers():
    if request.method == 'POST':
        fullname = (request.form['fullname']).split()
        last_name = fullname[0]
        first_name = fullname[1]
        middle_name = fullname[2]
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
    save it to the database.
    '''
    event = db_session.query(Event).get(id)
    if request.method == 'POST':
        try:
            fullname = (request.form['fullname']).split()
            event.last_name = fullname[0]
            event.first_name = fullname[1]
            event.middle_name = fullname[2]
            event.car_brand = request.form['car_brand']
            event.car_number = request.form['car_number']
            event.phone_number = request.form['phone_number']
            event.token = request.form['token']
            event.enter_date = request.form['enter_date']
            event.enter_time = request.form['enter_time']
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


@app.route('/journal/close_event/<int:id>')
@login_required
def close_event(id):
    event = db_session.query(Event).get(id)
    now = datetime.now()
    departure_date = now.strftime('%Y-%m-%d')
    departure_time = now.strftime('%H:%M:%S')
    delta = date.today() - event.enter_date
    total_days = delta.days
    after_payment = calculate_payment(event.lot_type, total_days)

    event.departure_date = departure_date
    event.departure_time = departure_time
    event.total_days = total_days
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
    Retrieve data from customer edit form and
    save it to the database.
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
    db_session.delete(event)
    db_session.commit()
    return redirect(url_for('journal'))


@app.route('/customers/delete/<int:id>')
@login_required
def delete_customer(id):
    '''
    Delete customer on button click.
    '''
    customer = db_session.query(Customer).get(id)
    db_session.delete(customer)
    db_session.commit()
    return redirect(url_for('customers'))


if __name__ == '__main__':
    app.run(debug=True)
