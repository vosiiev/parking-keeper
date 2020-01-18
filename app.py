from sqlalchemy import create_engine
from flask import Flask, Response, render_template, request, redirect, \
                    session, url_for, escape, abort
from sqlalchemy.orm import sessionmaker
from data import Event, User
from flask_login import LoginManager, login_required, \
                        login_user, logout_user, current_user
from flask_user import roles_required
from security import hash_password, verify_password
import logging


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
    '''
    if request.method == 'POST':
        fullname = request.form['fullname']
        car_brand = request.form['car_brand']
        car_number = request.form['car_number']
        phone_number = request.form['phone_number']
        enter_date = request.form['enter_date']
        enter_time = request.form['enter_time']
        pre_payment = request.form['pre_payment']
        token = request.form['token']
        departure_date = request.form['departure_date']
        departure_time = request.form['departure_time']
        total_days = request.form['total_days']
        after_payment = request.form['after_payment']
        new_event = Event(
                fullname=fullname,
                car_brand=car_brand,
                car_number=car_number,
                phone_number=phone_number,
                enter_date=enter_date,
                enter_time=enter_time,
                pre_payment=pre_payment,
                token=token,
                departure_date=departure_date,
                departure_time=departure_time,
                total_days=total_days,
                after_payment=after_payment,
            )
        db_session.add(new_event)
        db_session.commit()
        return redirect(url_for('journal'))
    else:
        events = db_session.query(Event).all()
        return render_template('journal.html', events=events)


@app.route('/customers')
def clients():
    return render_template('customers.html')


@app.route('/client')
def client():
    return render_template('client.html')


@app.route('/journal/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit(id):
    '''
    Retrieve data from journal event edit form and
    save it to the database.
    '''
    event = db_session.query(Event).get(id)
    if request.method == 'POST':
        event.fullname = request.form['fullname']
        event.car_brand = request.form['car_brand']
        event.car_number = request.form['car_number']
        event.phone_number = request.form['phone_number']
        event.enter_date = request.form['enter_date']
        event.enter_time = request.form['enter_time']
        event.pre_payment = request.form['pre_payment']
        event.token = request.form['token']
        event.departure_date = request.form['departure_date']
        event.departure_time = request.form['departure_time']
        event.total_days = request.form['total_days']
        event.after_payment = request.form['after_payment']
        db_session.commit()
        return redirect(url_for('journal'))
    else:
        return render_template('journal.html', edit_event=event)


@app.route('/journal/delete/<int:id>')
def delete(id):
    '''
    Delete journal event on button click.
    '''
    event = db_session.query(Event).get(id)
    db_session.delete(event)
    db_session.commit()
    return redirect(url_for('journal'))


if __name__ == '__main__':
    app.run(debug=True)
