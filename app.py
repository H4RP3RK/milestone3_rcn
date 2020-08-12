import os
from flask import Flask, render_template, redirect, request, url_for
from flask_pymongo import PyMongo 
from bson.objectid import ObjectId 
from os import path
if path.exists("env.py"):
    import env

app = Flask(__name__)

app.config["MONGO_DBNAME"] = os.environ.get("MONGO_DBNAME")
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")

mongo = PyMongo(app)

@app.route('/')
@app.route('/get_queries')
def get_queries():
    return render_template("queries.html", queries = mongo.db.queries.find())

@app.route('/new_query')
def new_query():
    return render_template("newquery.html")

@app.route("/submit_query", methods=["POST"])
def submit_query():
    query = mongo.db.contacts
    query.insert_one(request.form.to_dict())
    return redirect(url_for('get_queries'))

if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
    port=int(os.environ.get('PORT')),
    debug=True)