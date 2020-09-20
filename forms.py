# Took inspiration from Pretty Printed YouTube videos: https://www.youtube.com/watch?v=jR2aFKuaOBs

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField, DateTimeField
from wtforms.validators import DataRequired, Email, Length, EqualTo
from wtforms.widgets import TextArea


class registrationForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    telephone = StringField('Telephone', validators=[Length(min=11)])
    employer = StringField('Employer')
    job_title = StringField('Job Title')
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password', message='Passwords must match')])
    submit = SubmitField('Sign Up')


class loginForm(FlaskForm):
    username = StringField('email', validators=[DataRequired(), Email()])
    password = PasswordField('password', validators=[DataRequired()])
    submit = SubmitField('Login')


class accountForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    username = StringField('Username', validators=[DataRequired(), Email()])
    telephone = StringField('Telephone', validators=[Length(min=11)])
    employer = StringField('Employer')
    job_title = StringField('Job Title')
    submit = SubmitField('Update')


class workplaceForm(FlaskForm):
    workplace = SelectField('Workplace', choices=[('Belfast'), ('Cardiff'), ('Edinburgh'), ('Glasgow'), ('London'), ('West Midlands'), ('Yorkshire')])


class questionForm(FlaskForm):
    question_type = SelectField('Question Type', choices=[('Work Issue'), ('Professional Nursing Advice'), ('Careers')])
    question_details = StringField('Question Details', widget=TextArea(), validators=[DataRequired()])
    submit = SubmitField('Submit')


class contactForm(FlaskForm):
    contact_from = StringField('From')
    contact_to = StringField('To')
    contact_details = StringField('Question Details', widget=TextArea(), validators=[DataRequired()])
    submit = SubmitField('Submit')


class detailedContactForm(FlaskForm):
    contact_type = SelectField('Contact Type', choices=['Database', 'Email', 'In Person', 'Telephone', 'Teleconference', 'Videoconference'])
    contact_from = StringField('From')
    contact_to = StringField('To')
    contact_date = DateTimeField('Date', format='%d-%m-%Y %H:%M')
    contact_details = StringField('Contact Details', widget=TextArea(), validators=[DataRequired()])
    submit = SubmitField('Submit')
