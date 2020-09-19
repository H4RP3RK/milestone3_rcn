import os
import datetime
from flask import Flask, render_template, redirect, request, url_for, flash, session
from forms import loginForm, registrationForm, accountForm, workplaceForm, questionForm, contactForm, detailedContactForm
from flask_pymongo import PyMongo
from flask_bcrypt import Bcrypt
from bson.objectid import ObjectId
from os import path
if path.exists('env.py'):
    import env

app = Flask(__name__)

app.config['MONGO_DBNAME'] = os.environ.get('MONGO_DBNAME')
app.config['MONGO_URI'] = os.environ.get('MONGO_URI')
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')

mongo = PyMongo(app)
bcrypt = Bcrypt(app)

# PAGES SHARED BY MEMBERS AND STAFF


# Login - site opens on login page as site only intended for existing RCN members and RCN staff
@app.route('/', methods=['GET', 'POST'])
def shared_login():
    form = loginForm()
    users = mongo.db.users
    if 'username' in session:
        user = users.find_one({'username': session['username']})
        return redirect(url_for('home', username=session['username']))
    elif form.validate_on_submit():
        user = users.find_one({'username': form.username.data})
        if user and bcrypt.check_password_hash(user['password'], form.password.data):
            session['username'] = form.username.data
            flash(f'Welcome {user["first_name"].capitalize()}. You are logged in to your {user["role"].capitalize()} account.', 'success')
            return redirect(url_for('home', username=session['username']))
        else:
            flash('Email/password combination is not recognised', 'danger')
            return render_template('shared_login.html', form=form, title='Login')
    return render_template('shared_login.html', form=form, title='Login')


# Logout
@app.route('/log_out')
def log_out():
    session.pop('username', None)
    flash('You are now logged out', 'success')
    return redirect(url_for('shared_login'))


# Register - same method used for member and staff register form
@app.route('/register/<role>', methods=['GET', 'POST'])
def register(role):
    form = registrationForm()
    workplace_form = workplaceForm()
    if 'username' in session:
        return redirect(url_for('home', username=session['username']))
    elif request.method == 'POST':
        if form.validate_on_submit():
            users = mongo.db.users
            current_user = users.find_one({'username': request.form['email']})
            if current_user is None:
                hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
                new_user = {
                    'role': role,
                    'first_name': form.first_name.data,
                    'last_name': form.last_name.data,
                    'username': form.email.data,
                    'email': form.email.data,
                    'telephone': form.telephone.data,
                    'job_title': form.job_title.data,
                    'password': hashed_password
                }
                users.insert_one(new_user)
                if role == 'member':
                    users.update_one({'_id': new_user['_id']},
                                    {"$set": {'employer': form.employer.data}})
                if role == 'staff':
                    users.update_one({'_id': new_user['_id']},
                                    {"$set": {'workplace': workplace_form.workplace.data}})
                session['username'] = form.email.data
                flash(f'{role.capitalize()} account created for {form.first_name.data}', 'success')
                return redirect(url_for('home', username=session['username']))
            else:
                flash(f'{form.email.data} is already registered. You can login by clicking the link below', 'danger')
        else:
            flash(f'Error submitting form: {form.errors}. Please contact IT on 01698428764.', 'danger')
    return render_template('register.html', form=form, workplace_form=workplace_form, title=f'{role.capitalize()} Sign Up', role=role)


# Home page - shows account details and member/staff questions
@app.route('/home/<username>')
def home(username):
    user = mongo.db.users.find_one({'username': username})
    if user['role'] == 'member':
        open_questions = mongo.db.questions.find({'$and':
                                        [{'member_id': username},
                                        {'end_date': {'$exists': False}}]
                                        }).sort('start_date', -1)
        closed_questions = mongo.db.questions.find({'$and':
                                        [{'member_id': username},
                                        {'end_date': {'$exists': True}}]
                                        }).sort('start_date', -1)
        open_question_message = "You haven't asked any questions yet. When you do, they will appear here"
        question_heading = "Your Questions"
    elif user['role'] == 'staff':
        open_questions = mongo.db.questions.find({'$and': [{'staff_id': username},
                                        {'end_date': {'$exists': False}}]
                                        }).sort('start_date', -1)
        closed_questions = mongo.db.questions.find({'$and': [{'staff_id': username},
                                        {'end_date': {'$exists': True}}]
                                        }).sort('start_date', -1)
        open_question_message = "You have no assigned cases. When you do, they will appear here"
        question_heading = "Your Assigned Questions"
    return render_template('home.html',
                            member=user,
                            open_questions=open_questions,
                            closed_questions=closed_questions,
                            role=user['role'],
                            open_question_message=open_question_message,
                            question_heading=question_heading,
                            title=f"{user['first_name'].capitalize()}'s {user['role'].capitalize()} Home Page")


# Account - allows user to edit account details
# Took inspiration from Corey Schafer YouTube tutorials: https://www.youtube.com/watch?v=803Ei2Sq-Zs&t=134s
@app.route('/account/<username>', methods=['GET', 'POST'])
def account(username):
    user = mongo.db.users.find_one({'username': username})
    role = user['role']
    form = accountForm()
    workplace_form = workplaceForm()
    if request.method == 'GET':
        form.username.data = user['username']
        form.email.data = user['email']
        form.telephone.data = user['telephone']
        form.job_title.data = user['job_title']
        if role == "member":
            form.employer.data = user['employer']
        elif role == "staff":
            workplace_form.workplace.data = user['workplace']
    elif form.validate_on_submit():
        mongo.db.users.update(
            {'username': username},
            {'$set':
                {
                'email': form.email.data,
                'telephone': form.telephone.data,
                'job_title': form.job_title.data
                }})
        if role == 'member':
            mongo.db.users.update(
                {'username': username},
                {'$set':
                    {
                        'employer': form.employer.data
                    }})
        elif role == 'staff':
            mongo.db.users.update(
                {'username': username},
                {'$set':
                    {
                        'workplace': workplace_form.workplace.data
                    }})
        flash("Your details are now updated.", 'success')
        return redirect(url_for('home', username=session['username']))
    else:
        flash(f"Error: {form.errors}. Please contact IT on 01698428764.", 'danger')
    return render_template('account.html', member=user, title="Edit Your Account Details", form=form, workplace_form=workplace_form, role=role)


# Adds a new contact onto an existing question. Member can send contact to RCN Lead and vice versa
@app.route('/new_contact/<question_id>', methods=['GET', 'POST'])
def new_contact(question_id):
    form = contactForm()
    question = mongo.db.questions.find_one({'_id': ObjectId(question_id)})
    contacts = mongo.db.contacts
    users = mongo.db.users
    user = users.find_one({'username': session['username']})
    member = users.find_one({'username': question['member_id']})
    staff = users.find_one({'username': question['staff_id']})
    if request.method == 'GET':
        form.contact_from.data = f"{user['first_name']} {user['last_name']}"
        if user['role'] == 'member': 
            form.contact_to.data = f"{staff['first_name']} {staff['last_name']}"
        elif user['role'] == 'staff':
            form.contact_to.data = f"{member['first_name']} {member['last_name']}"
    elif request.method == 'POST':
        if form.validate_on_submit():
            contacontact = {
                'question_id': ObjectId(question_id),
                'contact_type': 'database',
                'date': datetime.datetime.utcnow().strftime('%d/%m/%y  %H:%M'),
                'summary': form.contact_details.data,
                'from': form.contact_from.data,
                'to': form.contact_to.data,
                'recorded_by': session['username'],
                'recorded_on': datetime.datetime.utcnow().strftime('%d/%m/%y  %H:%M')
            }
            contacts.insert_one(contact)
            if user['role'] == 'member':
                mongo.db.questions.update(
                    {'_id': ObjectId(question_id)},
                    {'$unset':
                        {
                            'end_date': ''
                        }})
                flash("Thanks for getting in touch. Your RCN Lead will be in touch shortly. Check your contacts below for updates", 'success')
                return redirect(url_for('question_details', question_id=question['_id']))
            elif user['role'] == 'staff':
                mongo.db.questions
                flash("Contact made. Check your contacts below for updates", 'success')
                return redirect(url_for('staff_question_details', question_id=question['_id']))
            else:
                flash("Error with your account. Please contact IT on 01698428764.", 'danger')
    return render_template('new_contact.html', title='Contact Form', question=question, user=user, member=member, role=user['role'], form=form)


# User can edit their own contacts
@app.route('/edit_contact/<contact_id>', methods=['GET', 'POST'])
def edit_contact(contact_id):
    user = mongo.db.users.find_one({'username': session['username']})
    contact = mongo.db.contacts.find_one({'_id': ObjectId(contact_id)})
    question = mongo.db.questions.find_one({'_id': ObjectId(contact['question_id'])})
    form = contactForm()
    if request.method == 'GET':
        form.contact_from.data = contact['from']
        form.contact_to.data = contact['to']
        form.contact_details.data = contact['summary']
    elif form.validate_on_submit():
        mongo.db.contacts.update(
            {'_id': ObjectId(contact_id)},
            {'$set':
                {
                    'summary': form.contact_details.data
                }})
        flash("Your contact has been updated.", 'success')
        return redirect(url_for(f"{user['role']}_question_details", question_id=question['_id']))
    return render_template('new_contact.html', contact=contact, question=question, title='Edit Contact', role=user['role'], form=form, user=user)


# PAGES ONLY AVAILABLE TO MEMBERS
# Member can ask a question
@app.route('/new_question', methods=['GET', 'POST'])
def new_question():
    form = questionForm()
    user = mongo.db.users.find_one({'username': session['username']})
    if request.method == 'POST':
        if form.validate_on_submit():
            questions = mongo.db.questions
            question = {
                'member_id': session['username'],
                'question_type': form.question_type.data,
                'start_date': datetime.datetime.utcnow().strftime('%d/%m/%y  %H:%M'),
                'summary': form.question_details.data,
                'staff_id': 'unassigned'
            }
            questions.insert_one(question)
            flash("Thanks for your question. We'll respond shortly. You can click on your question below for updates.", 'success')
            return redirect(url_for('home', username=session['username'], role=user['role']))
        else:
            flash(f"Error submitting form: {form.errors}. Please contact IT on ", "danger")
    return render_template('new_question.html', title='Ask a New Question', role=user['role'], form=form)


# Shows member details of the question they've asked, include the RCN Lead for their question and any associated contacts from both themselves or RCN Lead
@app.route('/question_details/<question_id>')
def question_details(question_id):
    user = mongo.db.users.find_one({'username': session['username']})
    contacts = mongo.db.contacts.find({'question_id': ObjectId(question_id)}).sort('date', -1)
    question = mongo.db.questions.find_one({'_id': ObjectId(question_id)})
    staff = mongo.db.users.find_one({'username': question['staff_id']})
    return render_template('question_details.html', contacts=contacts, question=question, staff=staff, title="Question Details - Member View", role=user['role'])


# PAGES ONLY AVAILABLE TO STAFF
# Allows staff to close a question once it is complete
@app.route('/close_question/<question_id>', methods=['GET', 'POST'])
def close_question(question_id):
    mongo.db.questions.update(
        {'_id': ObjectId(question_id)},
        {'$set':
            {
                'end_date': request.form.get('end_date')
            }})
    flash('Case now closed', 'success')
    return redirect(url_for('staff_question_details', question_id=question_id))


# Staff can reopen a closed question
@app.route('/reopen_question/<question_id>', methods=['GET', 'POST'])
def reopen_question(question_id):
    mongo.db.questions.update(
        {'_id': ObjectId(question_id)},
        {'$unset':
            {
                'end_date': ""
            }})
    flash('Case reopened', 'success')
    return redirect(url_for('staff_question_details', question_id=question_id))


@app.route('/unassigned_questions', methods=['GET', 'POST'])
def unassigned_questions():
    user = mongo.db.users.find_one({'username': session['username']})
    questions = mongo.db.questions
    unassigned = list(questions.find({'staff_id': 'unassigned'}).sort('start_date', 1))
    staff_list = list(mongo.db.users.find({'role': 'staff'}))
    if request.method == 'POST':
        questions.update(
            {'_id': ObjectId(request.form.get('question_id'))},
            {'$set':
                {'staff_id': request.form.get('staff_id')}})
        flash(f'Question assigned to {request.form.get("staff_id")}', 'success')
        return redirect(url_for('unassigned_questions'))
    return render_template('unassigned_questions.html', unassigned=unassigned, title='Unassigned Questions', staff_list=staff_list, role=user['role'])


@app.route('/staff_question_details/<question_id>', methods=['GET', 'POST'])
def staff_question_details(question_id):
    user = mongo.db.users.find_one({'username': session['username']})
    contacts = mongo.db.contacts.find({'question_id': ObjectId(question_id)}).sort('date', -1)
    question = mongo.db.questions.find_one({'_id': ObjectId(question_id)})
    member = mongo.db.users.find_one({'username': question['member_id']})
    staff = mongo.db.users.find_one({'username': question['staff_id']})
    staff_list = mongo.db.users.find({'role': 'staff'})
    if request.method == 'POST':
        mongo.db.questions.update(
            {'_id': ObjectId(request.form.get('question_id'))},
            {'$set':
                {'staff_id': request.form.get('staff_id')}})
        flash(f'Question assigned to {request.form.get("staff_id")}', 'success')
        return redirect(url_for('staff_question_details', question_id=question_id))
    return render_template('staff_question_details.html', contacts=contacts, question=question, member=member, staff=staff, staff_list=staff_list, question_id=question_id, title='Question Details - Staff View', role=user['role'])


@app.route('/assign_lead/<question_id>', methods=['POST'])
def assign_lead(question_id):
    user = mongo.db.users.find_one({'username': session['username']})
    staff = mongo.db.users.find_one({'username': request.form.get('staff_id')})
    questions = mongo.db.questions
    question = questions.find_one({'_id': ObjectId(question_id)})
    questions.update(
        {'_id': ObjectId(question_id)},
        {'$set':
            {
                'staff_id': request.form.get('staff_id')
            }})
    flash(f"The question has been assigned to {staff['first_name']}. The question will appear on their Home Page", 'success')
    return redirect(url_for('staff_question_details', question=question, question_id=question_id), role=user['role'])


@app.route('/staff_new_contact/<question_id>', methods=['GET', 'POST'])
def staff_new_contact(question_id):
    form = detailedContactForm()
    user = mongo.db.users.find_one({'username': session['username']})
    contacts = mongo.db.contacts
    question = mongo.db.questions.find_one({'_id': ObjectId(question_id)})
    if request.method == 'GET':
        form.contact_from.data = f"{user['first_name']} {user['last_name']}"
    elif form.validate_on_submit():
        contact = {
            'question_id': ObjectId(question_id),
            'contact_type': form.contact_type.data,
            'date': request.form.get('picker'),
            'summary': form.contact_details.data,
            'from': form.contact_from.data,
            'to': form.contact_to.data,
            'recorded_by': session['username'],
            'recorded_on': datetime.datetime.utcnow().strftime('%d/%m/%y  %H:%M')
        }
        contacts.insert_one(contact)
        flash("Your contact has been added. The member can now view your contacts", 'success')
        return redirect(url_for('staff_question_details', question_id=question['_id']))
    return render_template('staff_new_contact.html', title='Add a Contact', question=question, role=user['role'], form=form)


@app.route('/member_list')
def member_list():
    user = mongo.db.users.find_one({'username': session['username']})
    members = mongo.db.users.find({'role': 'member'}).sort('last_name', 1)
    return render_template('member_list.html', members=members, role=user['role'])


@app.route('/member_details/<member_id>')
def member_details(member_id):
    user = mongo.db.users.find_one({'username': session['username']})
    member = mongo.db.users.find_one({'_id': ObjectId(member_id)})
    questions = mongo.db.questions.find({'member_id': member['username']})
    return render_template('member_details.html', title=f"{member['first_name']} {member['last_name']}'s Account Details - Staff View", member=member, questions=questions, role=user['role'])


if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT')),
            debug=True)
