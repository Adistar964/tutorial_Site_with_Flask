from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError
from flaskfile.models import User
from flask_login import current_user

class Register(FlaskForm):
	username = StringField('Username',validators=[DataRequired(), Length(min=3, max=20)])
	email = StringField('Email Address' ,validators=[DataRequired(), Email()])
	password = PasswordField('Password' ,validators=[DataRequired()])
	confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
	submit = SubmitField('Sign up')

	def validate_username(self, username):
		user = User.query.filter_by(username=username.data).first()
		if user:
			raise ValidationError('Username already taken, So try another one')

	def validate_email(self, email):
		user = User.query.filter_by(email=email.data).first()
		if user:
			raise ValidationError('Email address already taken, So try another one')


class Login(FlaskForm):
	username = StringField('Username',validators=[DataRequired(), Length(min=3, max=20)])
	password = PasswordField('Password', validators=[DataRequired()])
	forgot = BooleanField('Forgot Password?')
	submit = SubmitField('Sign in')

class update(FlaskForm):
	username = StringField('Username',validators=[DataRequired(), Length(min=3, max=20)])
	email = StringField('Email Address' ,validators=[DataRequired(), Email()])
	submit = SubmitField('Update Info')

	def validate_username(self, username):
		if username.data == current_user.username:
			raise ValidationError('This was the old username, so try another one')

	def validate_email(self, email):
		if email.data == current_user.email:
			raise ValidationError('This was the old email, so try another one')

class new_post(FlaskForm):
	title = StringField('Title', validators=[DataRequired()])
	content = TextAreaField('Content', validators=[DataRequired()])
	submit = SubmitField('Add Post')

