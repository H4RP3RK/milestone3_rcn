import os, datetime
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
                            questions=mongo.db.questions.find({'member_id': email}), 
                            title=f"{member['first_name']}'s Home Page")


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
        { '$set': 
            {
                'telephone': request.form.get('telephone')
            }
        })
    return redirect(url_for('account'))


@app.route('/get_queries/<email>')
def get_queries(email):
    members = mongo.db.members
    member = members.find_one({'email': email})
    return render_template('queries.html', 
                            questions=mongo.db.questions.find({'email': email}), 
                            title=f"{member['first_name']}'s Current/Old Questions")


@app.route('/new_question')
def new_question():
    return render_template('new_question.html', title='Ask a New Question')


@app.route('/submit_question', methods=['POST'])
def submit_question():
    questions = mongo.db.questions
    question = {
        'member_id': session['email'],
        'question_type': request.form.get('question_type'),
        'start_date': datetime.datetime.utcnow(),
        'summary': request.form.get('summary')
    }
    questions.insert_one(question)
    flash("Thanks for your question. We'll respond shortly. You can click on your question below for updates.", 'success')
    return redirect(url_for('member_home', email=session['email']))


@app.route('/question_details/<question_id>')
def question_details(question_id):
    contacts = mongo.db.contacts.find({'question_id': ObjectId(question_id)})
    question = mongo.db.questions.find_one({'_id': ObjectId(question_id)})
    return render_template('question_details.html', contacts=contacts, question=question)


@app.route('/new_contact')
def new_contact():
    return render_template('newcontact.html', title='Ask a New Question')


@app.route('/submit_contact', methods=['POST'])
def submit_contact():
    contacts = mongo.db.contacts
    member = members.find_one({'email': session['email']})
    contact = {
        'member_id': session['email'],
        'date': datetime.datetime.utcnow(),
        'details': request.form.get('summary'),
        'from': member['first_name'],
        'to': 'RCN'
    }
    contacts.insert_one(contact)
    return redirect(url_for('member_home', email=session['email']))


@app.route('/log_out')
def log_out():
    session.pop('email', None)
    flash('You are now logged out', 'success')
    return redirect(url_for('welcome'))


if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT')),
            debug=True)
