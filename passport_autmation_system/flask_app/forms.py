from flask_wtf import FlaskForm
from flask_wtf.file  import FileField, FileAllowed
from flask_login import current_user 
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flask_app.models import User

class RegistrationForm(FlaskForm):

	username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])

	email = StringField('Email', validators=[DataRequired(), Email()])

	password = PasswordField('Password', validators=[DataRequired()])

	confirm_password = PasswordField('Conform Password', validators=[DataRequired(), EqualTo('password')])

	submit = SubmitField('Sign Up')

	def validate_username(self,username):
		user = User.query.filter_by(username=username.data).first()
		if user:
			raise ValidationError('that username is taken.please choose the other one instead')

	def validate_emailemail(self,email):
		user = User.query.filter_by(email=email.data).first()
		if user:
			raise ValidationError('that email is taken.please choose the other one instead')

class LoginForm(FlaskForm):

	
	email = StringField('Email', validators=[DataRequired(), Email()])

	password = PasswordField('Password', validators=[DataRequired()])

	remember = BooleanField('Remember me')

	submit = SubmitField('Sign In')


class UpdateAccountForm(FlaskForm):

	username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])

	email = StringField('Email', validators=[DataRequired(), Email()])

	picture = FileField('Update Profile Picture', validators= [FileAllowed(['jpg', 'png'])])

	submit = SubmitField('Update')

	def validate_username(self,username):
		if username.data != current_user.username:	
			user = User.query.filter_by(username=username.data).first()
			if user:
				raise ValidationError('that username is taken.please choose the other one instead')

	def validate_emailemail(self,email):
		if email.data != current_user.email:
			user = User.query.filter_by(email=email.data).first()
			if user:
				raise ValidationError('that email is taken.please choose the other one instead')


class PassportForm(FlaskForm):

	name = StringField('Name', validators=[DataRequired(), Length(min=2, max=20)])

	email = StringField('Email', validators=[DataRequired(), Email()])

	passport_picture = FileField('Passport Picture', validators= [FileAllowed(['jpg', 'png'])])

	date_of_birth = StringField('Date Of Birth', validators = [DataRequired()])

	phone = StringField('Mobile', validators=[DataRequired()])

	address = TextAreaField('Address', validators=[DataRequired()])

	submit = SubmitField('Submit')

class AuthVerificationForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    submit = SubmitField('SEND')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError('There is no account with that email. You must register first.')

class VerifyForm(FlaskForm):
		verification = StringField('if verfied type VERIFIED', validators=[DataRequired()])

		submit = SubmitField('Submit')