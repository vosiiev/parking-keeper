from sqlalchemy import create_engine
from flask import Flask, render_template, request, redirect
from sqlalchemy.orm import sessionmaker
from data import Event


app = Flask(__name__)
engine = create_engine('mysql+mysqlconnector://p_user:R3cogn1se!@localhost/parking', echo=True)
Session = sessionmaker(bind=engine)
session = Session()

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/journal', methods=['GET', 'POST'])
def journal():
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
        session.add(new_event)
        session.commit()
        return redirect('/journal')
    else:
        events = session.query(Event).all()
        return render_template('journal.html', events=events)


@app.route('/clients')
def clients():
    return render_template('clients.html')


@app.route('/client')
def client():
    return render_template('client.html')


@app.route('/journal/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    event = session.query(Event).get(id)
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
        session.commit()
        return redirect('/journal')
    else:
        return render_template('journal.html', edit_event=event)




@app.route('/journal/delete/<int:id>')
def delete(id):
    event = session.query(Event).get(id)
    session.delete(event)
    session.commit()
    return redirect('/journal')


if __name__ == '__main__':
    app.run(debug=True)
