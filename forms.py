from flask_wtf import Form
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, Length

class SignupForm(Form):
	first_name = StringField('First Name', validators=[DataRequired('Please Enter Your First Name')])
	last_name  = StringField('Last Name', validators=[DataRequired('Please Enter Your Last Name')])
	email      = StringField('Email', validators=[DataRequired('Please Enter Your Email-ID'),
													Email('Enter a Valid Email-ID')])
	password   = PasswordField('Password', validators=[DataRequired('Please Enter a Password'),
													Length(min=6, message='Password must be atleast 6 Characters Long')])
	submit     = SubmitField('Sign Up')

class LoginForm(Form):
	email    = StringField('Email', validators=[DataRequired('Please Enter Your Email-ID'),
												Email('Enter a Valid Email-ID')])
	password = PasswordField('Password', validators=[DataRequired('Please Enter a Password')])
	submit   = SubmitField('Sign In')

class AddressForm(Form):
	address = StringField('Address', validators=[DataRequired('Please Enter an Adress')])
	submit  = SubmitField('Search')