from sqlalchemy import create_engine
from flask import Flask, render_template
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String

app = Flask(__name__)
engine = create_engine('mysql+mysqlconnector://p_user:R3cogn1se!@localhost/parking', echo=True)
Base = declarative_base()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/journal')
def journal():
    return render_template('journal.html')


@app.route('/clients.html')
def clients():
    return render_template('clients.html')


@app.route('/client.html')
def client():
    return render_template('client.html')


if __name__ == '__main__':
    app.run(debug=True)
