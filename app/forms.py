from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, EmailField, TextAreaField
from wtforms.validators import DataRequired, ValidationError, EqualTo, Email, Length
from app.models import User, Post


class RegistrationForm(FlaskForm):
	username = StringField(label='Username', validators=[DataRequired()])
	password = PasswordField(label='Password', validators=[DataRequired()])
	rpassword = PasswordField(label='Repeat password', validators=[DataRequired(),
																   EqualTo('password',
																			message='Passwords do not match')])
	email = EmailField(label='Email', validators=[DataRequired(), Email()])


	def validate_email(self, email):
		existent=User.query.filter_by(email=email.data).first()
		if existent:
			raise ValidationError('User already ')


class LoginForm(FlaskForm):
	email = StringField('Email', validators=[DataRequired()])
	password = PasswordField('Password', validators=[DataRequired()])
	submit = SubmitField('Sign in')

	def validate_submit(self, submit):
		user = User.query.filter_by(email=self.email.data).first()
		if not user or not user.check_password(self.password.data):
			raise ValidationError('email and password do not match')


class PostForm(FlaskForm):
	body = TextAreaField(label='Your message', validators=[Length(min=0, max=1000)])
	title = TextAreaField(label='title', validators=[Length(min=0, max=50)])



