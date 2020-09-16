import os, datetime
from flask import Flask, render_template, redirect, request, url_for, flash, session
from forms import loginForm, registrationForm, accountForm
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


@app.route('/')
def user_role(user_id):
    user = mongo.db.users.find_one({'_id': ObjectId(user_id)})
    role = user['role']

@app.route('/shared_login', methods=['GET', 'POST'])
def shared_login():
    form = loginForm()
    users = mongo.db.users
    if 'username' in session:
        user = users.find_one({'username': session['username']})
        return redirect(url_for('home', username=session['username']))
    if request.method == 'POST':
        if form.validate_on_submit():
            user = users.find_one({'username': form.username.data})
            if user and bcrypt.check_password_hash(user['password'], form.password.data):
                session['username'] = form.username.data
                flash(f'Welcome {user["first_name"].capitalize()}. You are logged in to your {user["role"].capitalize()} account.', 'success')
                return redirect(url_for('home', username=session['username']))
            else:
                flash('Email/password combination is not recognised', 'danger')
                return render_template('shared_login.html', form=form, title='Login')
        else:
            flash('Error logging in. Please refresh the page and try again.', 'danger')
    return render_template('shared_login.html', form=form, title='Login')


@app.route('/register/<role>', methods=['GET', 'POST'])
def register(role):
    if 'username' in session:
        return redirect(url_for('home', username=session['username']))
    form = registrationForm()
    if request.method == 'POST':
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
                                    {"$set": {'workplace': form.workplace.data}})
                session['username'] = form.email.data
                flash(f'{role.capitalize()} account created for {form.first_name.data}', 'success')
                return redirect(url_for('home', username=session['username']))
            else:
                flash(f'{form.email.data} is already registered. You can login by clicking the link below', 'danger')
        else:
            flash(f'Error submitting form: {form.errors} Please contact IT', 'danger')
    return render_template('register.html', form=form, title=f'{role.capitalize()} Sign Up', role=role)


@app.route('/home/<username>')
def home(username):
    user = mongo.db.users.find_one({'username': username})
    questions = mongo.db.questions.find({'$and': [{'member_id': username}, {'end_date': {'$exists': False}}]}).sort('start_date', -1)
    closed_questions = mongo.db.questions.find({'$and': [{'member_id': username}, {'end_date': {'$exists': True}}]}).sort('start_date', -1)
    assigned = mongo.db.questions.find({'$and': [{'staff_id': username}, {'end_date': {'$exists': False}}]}).sort('start_date', -1)
    closed_assigned = mongo.db.questions.find({'$and': [{'staff_id': username}, {'end_date': {'$exists': True}}]}).sort('start_date', -1)
    return render_template('home.html', 
                            member=user,
                            questions=questions, 
                            closed_questions=closed_questions,
                            assigned=assigned,
                            closed_assigned=closed_assigned,
                            role=user['role'],
                            title=f"{user['first_name'].capitalize()}'s {user['role'].capitalize()} Home Page")


# Took inspiration from Corey Schafer YouTube tutorials: https://www.youtube.com/watch?v=803Ei2Sq-Zs&t=134s

@app.route('/account/<username>', methods=['GET', 'POST'])
def account(username):
    user = mongo.db.users.find_one({'username': username})
    role = user['role']
    form = accountForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            mongo.db.users.update( 
                {'username': username}, 
                { '$set': 
                    {
                        'email': form.email.data,
                        'telephone': form.telephone.data,
                        'employer': form.employer.data,
                        'job_title': form.job_title.data
                    }
                })
            flash("Your details are now updated.", 'success')
            return redirect(url_for('home', username=session['username']))
        else:
            flash('Error submitting form. Please refresh the page and try again.', 'danger')
    elif request.method == 'GET':
        form.username.data = user['username']
        form.email.data = user['email']
        form.telephone.data = user['telephone']
        form.job_title.data = user['job_title']
        if role == "member":
            form.employer.data = user['employer']
        elif role == "staff":
            form.workplace.data = user['workplace']
        else:
            flash("Error with your account. Unsure whether you are an RCN member or staff. Please contact IT for support", 'danger')            
    return render_template('account.html', member=user, title="Edit Your Account Details", form=form, role=role)


@app.route('/new_contact/<question_id>', methods=['GET', 'POST'])
def new_contact(question_id):
    question = mongo.db.questions.find_one({'_id': ObjectId(question_id)})
    contacts = mongo.db.contacts
    users = mongo.db.users
    user = users.find_one({'username': session['username']})
    member = users.find_one({'username': question['member_id']})
    staff = users.find_one({'username': question['staff_id']})
    if request.method == 'POST':
        contact = {
            'question_id': ObjectId(question_id),
            'contact_type': 'database',
            'date': datetime.datetime.utcnow().strftime('%d/%m/%y  %H:%M'),
            'summary': request.form.get('summary'),
            'from': request.form.get('from'),
            'to': request.form.get('to'),
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
                    }
                })
            flash("Thanks for getting in touch. Your RCN Lead will be in touch shortly. Check your contacts below for updates", 'success')
            return redirect(url_for('question_details', question_id=question['_id']))
        elif user['role'] == 'staff':
            flash(f"Contact made. Check your contacts below for updates", 'success')
            return redirect(url_for('staff_question_details', question_id=question['_id']))
        else:
            flash("Problem with your account. Please contact IT", 'danger')           
    return render_template('new_contact.html', title='Contact Form', question=question, user=user, member=member, role=user['role'])


@app.route('/edit_contact/<contact_id>', methods=['GET', 'POST'])
def edit_contact(contact_id):
    contact = mongo.db.contacts.find_one({'_id': ObjectId(contact_id)})
    question = mongo.db.questions.find_one({'_id': ObjectId(contact['question_id'])})
    if request.method == 'POST':
        mongo.db.contacts.update( 
            {'_id': ObjectId(contact_id)}, 
            { '$set': 
                {
                    'summary': request.form.get('summary')
                }
            })
        flash("Your contact has been updated.", 'success')
        return redirect(url_for('question_details', question_id=question['_id']))        
    return render_template('edit_contact.html', contact=contact, question=question, title='Edit Contact') 


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
        'summary': request.form.get('summary'),
        'staff_id': 'unassigned'
    }
    questions.insert_one(question)
    flash("Thanks for your question. We'll respond shortly. You can click on your question below for updates.", 'success')
    return redirect(url_for('home', username=session['username']))


@app.route('/question_details/<question_id>')
def question_details(question_id):
    contacts = mongo.db.contacts.find({'question_id': ObjectId(question_id)}).sort('date', -1)
    question = mongo.db.questions.find_one({'_id': ObjectId(question_id)})
    staff = mongo.db.users.find_one({'username': question['staff_id']})
    return render_template('question_details.html', contacts=contacts, question=question, staff=staff, title="Question Details - Member View")


@app.route('/close_question/<question_id>', methods=['GET', 'POST'])
def close_question(question_id):
    question = mongo.db.questions.find_one({'_id': ObjectId(question_id)})
    mongo.db.questions.update( 
        {'_id': ObjectId(question_id)}, 
        { '$set': 
            {
                'end_date': request.form.get('end_date')
            }
        })
    flash('Case now closed', 'success')
    return redirect(url_for('staff_question_details', question_id=question_id))


@app.route('/reopen_question/<question_id>', methods=['GET', 'POST'])
def reopen_question(question_id):
    mongo.db.questions.update( 
        {'_id': ObjectId(question_id)}, 
        { '$unset': 
            {
                'end_date': ""
            }
        })
    flash('Case reopened', 'success')
    return redirect(url_for('staff_question_details', question_id=question_id))    


@app.route('/log_out')
def log_out():
    session.pop('username', None)
    flash('You are now logged out', 'success')
    return redirect(url_for('shared_login'))


#STAFF SIDE OF SITE


@app.route('/unassigned_questions', methods=['GET','POST'])
def unassigned_questions():
    questions = mongo.db.questions
    unassigned = list(questions.find({'staff_id': 'unassigned'}).sort('start_date', 1))
    staff_list = list(mongo.db.users.find({'role': 'staff'}))
    if request.method == 'POST':
        questions.update(
            {'_id': ObjectId(request.form.get('question_id'))},
            { '$set': 
                {'staff_id': request.form.get('staff_id')}
            }
        )
        flash(f'Question assigned to {request.form.get("staff_id")}', 'success')
        return redirect(url_for('unassigned_questions'))
    return render_template('unassigned_questions.html', unassigned=unassigned, title='Unassigned Questions', staff_list=staff_list)


@app.route('/staff_question_details/<question_id>', methods=['GET', 'POST'])
def staff_question_details(question_id):
    contacts = mongo.db.contacts.find({'question_id': ObjectId(question_id)}).sort('date', -1)
    question = mongo.db.questions.find_one({'_id': ObjectId(question_id)})
    member = mongo.db.users.find_one({'username': question['member_id']})
    staff = mongo.db.users.find_one({'username': question['staff_id']})
    staff_list = mongo.db.users.find({'role': 'staff'})
    if request.method == 'POST':
        mongo.db.questions.update(
            {'_id': ObjectId(request.form.get('question_id'))},
            { '$set': 
                {'staff_id': request.form.get('staff_id')}
            }
        )
        flash(f'Question assigned to {request.form.get("staff_id")}', 'success')
        return redirect(url_for('staff_question_details', question_id=question_id))
    return render_template('staff_question_details.html', contacts=contacts, question=question, member=member, staff=staff, staff_list=staff_list, question_id=question_id, title='Question Details - Staff View')


@app.route('/assign_lead/<question_id>', methods=['POST'])
def assign_lead(question_id):
    staff = mongo.db.users.find_one({'username': request.form.get('staff_id')})
    questions = mongo.db.questions
    question = questions.find_one({'_id': ObjectId(question_id)})
    questions.update(
        {'_id': ObjectId(question_id)},
        { '$set':
            {
                'staff_id': request.form.get('staff_id')
            }
        })
    flash(f"The question has been assigned to {staff['first_name']}. The question will appear on their Home Page", 'success')
    return redirect(url_for('staff_question_details', question=question, question_id=question_id))


@app.route('/staff_new_contact/<question_id>', methods=['GET', 'POST'])
def staff_new_contact(question_id):
    contacts = mongo.db.contacts
    question = mongo.db.questions.find_one({'_id': ObjectId(question_id)})
    member = mongo.db.members.find_one({'username': question['member_id']})
    if request.method == 'POST':
        contact = {
            'member_id': question['member_id'],
            'question_id': ObjectId(question_id),
            'contact_type': request.form.get('contact_type'),
            'date': request.form.get('date'),
            'summary': request.form.get('summary'),
            'from': request.form.get('from'),
            'to': request.form.get('to'),
            'recorded_by': session['username'],
            'recorded_on': datetime.datetime.utcnow().strftime('%d/%m/%y  %H:%M')
        }
        contacts.insert_one(contact)
        flash("Your contact has been added. The member can now view your contacts", 'success')
        return redirect(url_for('staff_question_details', question_id=question['_id']))
    return render_template('staff_new_contact.html', title='Add a Contact', question=question)


@app.route('/member_list')
def member_list():
    members = mongo.db.users.find({'role': 'member'})
    return render_template('member_list.html', members=members)

@app.route('/member_details/<member_id>')
def member_details(member_id):
    member = mongo.db.users.find_one({'_id': ObjectId(member_id)})
    questions = mongo.db.questions.find({'member_id': member['username']})
    return render_template('member_details.html', title=f"{member['first_name']} {member['last_name']}'s Account Details - Staff View", member=member, questions=questions)


# SHARED SITE


if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT')),
            debug=True)
