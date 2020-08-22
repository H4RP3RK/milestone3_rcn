import os
from flask import Flask, render_template, redirect, request, url_for
from forms import registrationForm, loginForm
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from os import path
if path.exists('env.py'):
    import env

app = Flask(__name__)

app.config['MONGO_DBNAME'] = os.environ.get('MONGO_DBNAME')
app.config['MONGO_URI'] = os.environ.get('MONGO_URI')
app.config['SECRET_KEY'] = os.environ['SECRET_KEY']

mongo = PyMongo(app)


@app.route('/')
@app.route('/welcome')
def welcome():
    return render_template('welcome.html')


@app.route('/welcome_member')
def welcome_member():
    return render_template('welcome_member.html')


@app.route('/register')
def register():
    registrationForm = registrationForm()
    return render_template('register.html', form=registrationForm)


@app.route('/log_in')
def log_in():
    loginForm = loginForm()
    return render_template('log_in.html', form=loginForm)


@app.route('/signup')
def signup():
    return render_template('signup.html')


@app.route('/signup_send', methods=['POST'])
def signup_send():
    member = mongo.db.members
    member.insert_one(request.form.to_dict())
    return redirect(url_for('login'))


@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/new_contact')
def new_contact():
    return render_template('newcontact.html')


@app.route('/get_queries')
def get_queries():
    return render_template('queries.html', queries=mongo.db.queries.find())


@app.route('/submit_contact', methods=['POST'])
def submit_contact():
    contact = mongo.db.contacts
    contact.insert_one(request.form.to_dict())
    return redirect(url_for('get_queries'))


if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT')),
            debug=True)
