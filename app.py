import os
from flask import Flask, render_template, redirect, request, url_for, flash, session
from forms import registrationForm, loginForm
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from os import path
if path.exists('env.py'):
    import env

app = Flask(__name__)

app.config['MONGO_DBNAME'] = os.environ.get('MONGO_DBNAME')
app.config['MONGO_URI'] = os.environ.get('MONGO_URI')
app.config['SECRET_KEY'] = ' '

mongo = PyMongo(app)


@app.route('/')
@app.route('/welcome')
def welcome():
    return render_template('welcome.html', title='Welcome to the RCN Member Query Database')


@app.route('/log_in', methods=['GET', 'POST'])
def log_in():
    form = loginForm()
    if request.method == 'POST':
        members = mongo.db.members
        member = members.find_one({'email': form.email.data})
        if member:
            if member['password'] == form.password.data:
                session['email'] = form.email.data
                flash(f'You are logged in, {member["first_name"]}!', 'success')
                return redirect(url_for('member_home', email=session['email']))
            else:
                flash('Email/password combination is not recognised', 'danger')
                return render_template('log_in.html', form=form, title='Member Login')
        else:
            flash('Email/password combination is not recognised', 'danger')
            return render_template('log_in.html', form=form, title='Member Login')
    return render_template('log_in.html', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = registrationForm()
    if request.method == 'POST':
        members = mongo.db.members
        current_member = members.find_one({'email': request.form['email']})

        if current_member is None:
            members.insert_one(request.form.to_dict())
            session['email'] = form.email.data
            flash(f'Account created for {form.first_name.data}', 'success')
            return redirect(url_for('member_home', email=session['email']))
        else:
            flash(f'{form.email.data} is already registered. Reset your password', 'danger')
            return render_template('register.html', form=form, title='Sign Up')
    return render_template('register.html', form=form, title='Sign Up')


@app.route('/member_home/<email>')
def member_home(email):
    members = mongo.db.members
    member = members.find_one({'email': email})
    return render_template('member_home.html', 
                            member=member, 
                            member_name=member['first_name'], 
                            title=f"{member['first_name']}'s Home Page")


@app.route('/new_contact')
def new_contact():
    return render_template('newcontact.html')


@app.route('/get_queries/<email>')
def get_queries(email):
    return render_template('queries.html', queries=mongo.db.queries.find({'email': email}), title='Your Current/Old Questions')


@app.route('/submit_contact', methods=['POST'])
def submit_contact():
    contact = mongo.db.contacts
    contact.insert_one(request.form.to_dict())
    return redirect(url_for('get_queries'))


if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT')),
            debug=True)
