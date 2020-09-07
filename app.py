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
    if 'username' in session:
        return redirect(url_for('member_home', username=session['username']))
    form = loginForm()
    if request.method == 'POST':
        members = mongo.db.members
        member = members.find_one({'username': form.email.data})
        if member:
            if bcrypt.check_password_hash(member['password'], form.password.data):
                session['username'] = form.email.data
                flash(f'You are logged in, {member["first_name"]}!', 'success')
                return redirect(url_for('member_home', username=session['username']))
            else:
                flash('Email/password combination is not recognised', 'danger')
                return render_template('log_in.html', form=form, title='Member Login')
        else:
            flash('Email/password combination is not recognised', 'danger')
            return render_template('log_in.html', form=form, title='Member Login')
    return render_template('log_in.html', form=form, title='Member Login')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if 'username' in session:
        return redirect(url_for('member_home', email=session['username']))
    form = registrationForm()
    if request.method == 'POST':
        members = mongo.db.members
        current_member = members.find_one({'username': request.form['email']})

        if current_member is None:
            hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
            new_member = {
                'first_name': form.first_name.data,
                'last_name': form.last_name.data,
                'username': form.email.data,
                'email': form.email.data,
                'telephone': form.telephone.data,
                'employer': form.employer.data,
                'job_title': form.job_title.data,
                'password': hashed_password
            }
            members.insert_one(new_member)
            session['username'] = form.email.data
            flash(f'Account created for {form.first_name.data}', 'success')
            return redirect(url_for('member_home', username=session['username']))
        else:
            flash(f'{form.email.data} is already registered. You can login by clicking the link below', 'danger')
    return render_template('register.html', form=form, title='Sign Up')


@app.route('/new_contact/<question_id>', methods=['GET', 'POST'])
def new_contact(question_id):
    contacts = mongo.db.contacts
    question = mongo.db.questions.find_one({'_id': ObjectId(question_id)})
    member = mongo.db.members.find_one({'email': session['email']})
    if request.method == 'POST':
        contact = {
            'member_id': session['email'],
            'question_id': ObjectId(question_id),
            'contact_type': 'database',
            'date': datetime.datetime.utcnow().strftime('%d/%m/%y  %H:%M'),
            'summary': request.form.get('summary'),
            'from': member['first_name'],
            'to': 'RCN'
        }
        contacts.insert_one(contact)
        flash("Thanks for getting in touch. Your RCN Lead will be in touch shortly. Check your contacts below for updates", 'success')
        return redirect(url_for('question_details', question_id=question['_id']))
    return render_template('newcontact.html', title='Contact your RCN Lead', question=question)


@app.route('/member_home/<username>')
def member_home(username):
    members = mongo.db.members
    member = members.find_one({'username': username})
    return render_template('member_home.html', 
                            member=member, 
                            member_name=member['first_name'],
                            questions=mongo.db.questions.find({'member_id': username}), 
                            title=f"{member['first_name']}'s Home Page")


@app.route('/account/<username>')
def account(username):
    members = mongo.db.members
    member = members.find_one({'username': username})
    return render_template('account.html', 
                            member=member,
                            title=f"{member['first_name']}'s Account")


@app.route('/edit_account/<username>', methods=['GET', 'POST'])
def edit_account(username):
    members = mongo.db.members
    members.update( 
        {'username': username}, 
        { '$set': 
            {
                'email': request.form.get('email'),
                'telephone': request.form.get('telephone'),
                'employer': request.form.get('employer'),
                'job_title': request.form.get('job_title')
            }
        })
    flash("Your details are now updated.", 'success')
    return redirect(url_for('account', username=session['username']))


@app.route('/new_question')
def new_question():
    return render_template('new_question.html', title='Ask a New Question')


@app.route('/submit_question', methods=['POST'])
def submit_question():
    questions = mongo.db.questions
    question = {
        'member_id': session['username'],
        'question_type': request.form.get('question_type'),
        'start_date': datetime.datetime.utcnow().strftime('%d/%m/%y  %H:%M'),
        'summary': request.form.get('summary')
    }
    questions.insert_one(question)
    flash("Thanks for your question. We'll respond shortly. You can click on your question below for updates.", 'success')
    return redirect(url_for('member_home', username=session['username']))


@app.route('/question_details/<question_id>')
def question_details(question_id):
    contacts = mongo.db.contacts.find({'question_id': ObjectId(question_id)})
    question = mongo.db.questions.find_one({'_id': ObjectId(question_id)})
    return render_template('question_details.html', contacts=contacts, question=question)


@app.route('/log_out')
def log_out():
    session.pop('username', None)
    flash('You are now logged out', 'success')
    return redirect(url_for('welcome'))


if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT')),
            debug=True)
