import os
from flask import Flask, render_template, redirect, request, url_for
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from os import path
if path.exists('env.py'):
    import env

app = Flask(__name__)

app.config['MONGO_DBNAME'] = os.environ.get('MONGO_DBNAME')
app.config['MONGO_URI'] = os.environ.get('MONGO_URI')

mongo = PyMongo(app)


@app.route('/')


@app.route('/signup')
def signup():
    return render_template('signup.html')


@app.route('/signup_send', methods=['POST'])
def signup_send():
    member = mongo.db.members
    member.insert_one(request.form.to_dict())
    return redirect(url_for('new_contact'))


@app.route('/get_queries')
def get_queries():
    return render_template('queries.html', queries=mongo.db.queries.find())


@app.route('/new_contact')
def new_query():
    return render_template('newcontact.html')


@app.route('/submit_contact', methods=['POST'])
def submit_contact():
    contact = mongo.db.contacts
    contact.insert_one(request.form.to_dict())
    return redirect(url_for('get_queries'))


if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT')),
            debug=True)
