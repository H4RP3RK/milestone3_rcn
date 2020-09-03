import os
from flask import Flask, render_template, redirect, request, url_for, flash, session
from forms import registrationForm, loginForm
from flask_pymongo import PyMongo
from flask_bcrypt import Bcrypt
from bson.objectid import ObjectId
from os import path
if path.exists('env.py'):
    import env

app = Flask(__name__)

app.config['MONGO_DBNAME'] = os.environ.get('MONGO_DBNAME')
app.config['MONGO_URI'] = os.environ.get('MONGO_URI')
app.config['SECRET_KEY'] = ' '

mongo = PyMongo(app)
bcrypt = Bcrypt(app)


@app.route('/')
@app.route('/welcome')
def welcome():
    return render_template('welcome.html', title='Welcome to the RCN Member Query Database')


@app.route('/log_in', methods=['GET', 'POST'])
def log_in():
    if 'email' in session:
        return redirect(url_for('member_home', email=session['email']))
    form = loginForm()
    if request.method == 'POST':
        members = mongo.db.members
        member = members.find_one({'email': form.email.data})
        if member:
            if bcrypt.check_password_hash(member['password'], form.password.data):
                session['email'] = form.email.data
                flash(f'You are logged in, {member["first_name"]}!', 'success')
                return redirect(url_for('member_home', email=session['email']))
            else:
                flash('Email/password combination is not recognised', 'danger')
                return render_template('log_in.html', form=form, title='Member Login')
        else:
            flash('Email/password combination is not recognised', 'danger')
            return render_template('log_in.html', form=form, title='Member Login')
    return render_template('log_in.html', form=form, title='Member Login')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if 'email' in session:
        return redirect(url_for('member_home', email=session['email']))
    form = registrationForm()
    if request.method == 'POST':
        members = mongo.db.members
        current_member = members.find_one({'email': request.form['email']})

        if current_member is None:
            hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
            new_member = {
                'first_name': form.first_name.data,
                'last_name': form.last_name.data,
                'email': form.email.data,
                'telephone': form.telephone.data,
                'employer': form.employer.data,
                'job_title': form.job_title.data,
                'password': hashed_password
            }
            members.insert_one(new_member)
            session['email'] = form.email.data
            flash(f'Account created for {form.first_name.data}', 'success')
            return redirect(url_for('member_home', email=session['email']))
        else:
            flash(f'{form.email.data} is already registered. You can login by clicking the link below', 'danger')
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
    return render_template('newcontact.html', title='Ask a New Question')


@app.route('/account/<email>')
def account(email):
    members = mongo.db.members
    member = members.find_one({'email': email})
    return render_template('account.html', 
                            member=member,
                            title=f"{member['first_name']}'s Account")


@app.route('/edit_account/<email>', methods=['GET', 'POST'])
def edit_account(email):
    members = mongo.db.members
    members.update( 
        {'email': email}, 
        { $set: 
            {
                'telephone': request.form.get('telephone'),
            }
        })
    return redirect(url_for('account'))


@app.route('/get_queries/<email>')
def get_queries(email):
    members = mongo.db.members
    member = members.find_one({'email': email})
    return render_template('queries.html', 
                            queries=mongo.db.queries.find({'email': email}), 
                            title=f"{member['first_name']}'s Current/Old Questions")


@app.route('/submit_contact', methods=['POST'])
def submit_contact():
    contact = mongo.db.contacts
    contact.insert_one(request.form.to_dict())
    return redirect(url_for('get_queries'))


@app.route('/log_out')
def log_out():
    session.pop('email', None)
    flash('You are now logged out', 'success')
    return redirect(url_for('welcome'))


if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT')),
            debug=True)
