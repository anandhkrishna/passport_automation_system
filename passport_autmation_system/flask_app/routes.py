import os
import secrets
from flask import render_template, url_for, flash, redirect, request
from flask_app import app, db, mail
from flask_app.forms import RegistrationForm, LoginForm, UpdateAccountForm, PassportForm, AuthVerificationForm, VerifyForm
from flask_app.models import User, Passport
from flask_login import login_user, current_user, logout_user, login_required
from flask_mail import Message

about_me=[
		{
			'author':'anandhkrishna',
			'title':'passport automation system',
			'email':'anandhkrishnauk@gmail.com'		
		}
		
	  ]

@app.route('/')
def dashboard():
	return render_template('dashboard.html')

@app.route('/home', methods=['GET'])
def home():
	passports = Passport.query.all()
	return render_template('home.html', passports = passports)

@app.route('/about')
def about():
	return render_template('about.html', about_me=about_me, title='About')

@app.route('/register', methods=['GET', 'POST'])
def register():
		if current_user.is_authenticated:
			return redirect(url_for('home'))
		form = RegistrationForm()
		if form.validate_on_submit():
			user = User(username=form.username.data, email=form.email.data, password=form.password.data)
			db.session.add(user)
			db.session.commit()
			flash(f'Account created for {form.username.data} and now you can log in!', 'success')
			return redirect(url_for('login'))
		return render_template('register.html', title='Register', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
		if current_user.is_authenticated:
			return redirect(url_for('dashboard'))


		form = LoginForm()
		if form.validate_on_submit():
			if form.email.data == 'admin@blog.com' and form.password.data == 'admin':
				flash('You have been logged in!', 'success')
				return redirect(url_for('home'))
			else:
				user = User.query.filter_by(email= form.email.data).first()
			if user and user.password == form.password.data:
				login_user(user, remember=form.remember.data)
				return redirect(url_for('account'))
			else :
				flash('login Unsuccessful. Please check username and password', 'danger')

		return render_template('login.html', title='Login', form=form)
@app.route('/logout')
def logout():
		logout_user()
		return redirect(url_for('dashboard'))


def save_picture(form_picture):
	random_hex = secrets.token_hex(8)
	_, f_ext = os.path.splitext(form_picture.filename)
	picture_fn = random_hex + f_ext
	picture_path = os.path.join(app.root_path, 'static/pics', picture_fn)
	form_picture.save(picture_path)
	return picture_fn

@app.route('/account', methods=['GET', 'POST'])
@login_required
def account():
		form = UpdateAccountForm()
		if form.validate_on_submit():
			if form.picture.data:
				picture_file = save_picture(form.picture.data)
				current_user.image_file = picture_file

			current_user.username = form.username.data
			current_user.email = form.email.data
			db.session.commit()
			flash('your account has been updated', 'success')
			return redirect(url_for('account'))
		elif request.method == 'GET':
			form.username.data = current_user.username
			form.email.data = current_user.email
		image_file = url_for('static', filename='pics/'+ current_user.image_file)
		return render_template('account.html', title='Account', image_file=image_file, form = form)



@app.route('/passport/new', methods=['GET', 'POST'])
@login_required
def new_passport():
	form = PassportForm()
	if form.validate_on_submit():
		if form.passport_picture.data:
			pass_pic = save_picture(form.passport_picture.data)

		else:
			return "no picture uloaded", 400


		passport = Passport(name = form.name.data, email= form.email.data, 
			passport_picture= pass_pic, date_of_birth= form.date_of_birth.data, 
			phone=form.phone.data, address=form.address.data, author = current_user)
		db.session.add(passport)
		db.session.commit()
		flash(f'your passport has been submitted', 'success')
		return redirect(url_for('dashboard'))
	return render_template('create_passport.html', title='Passport', form = form)


@app.route('/passport/<int:passport_id>')
def passport(passport_id):
	passport= Passport.query.get_or_404(passport_id)
	return render_template('passport.html', passport = passport)



@app.route('/passport/<int:passport_id>')
def reject_passport(passport_id):
	passport= Passport.query.get_or_404(passport_id)
	db.delete(passport)
	db.session.commit()
	flash('passport rejected successfully', 'success')
	return redirect(url_for('home'))

def send_mail(user):
		msg = Message('PASSPORT SYSTEM', sender = 'anandhkrishnauk@gmail.com', recipients= [user.email])

		msg.body = f'''passport will be dispatched soon ''' 
		mail.send(msg)

def send_verification_mail(user):
	token = user.get_reset_token()
	msg = Message('PASSPORT SYSTEM', sender = 'anandhkrishnauk@gmail.com', recipients= ['trichypolicekarar@gmail.com'])

	msg.body =f'''verify link here:{url_for('verify', token = token, _external = True)}

				applicnt details:{url_for('applicant', token = token, _external=True)}

	''' 
	mail.send(msg)

@app.route("/auth_verification", methods=['GET', 'POST'])
def verification():
	form = AuthVerificationForm()
	if form.validate_on_submit():
		user = Passport.query.filter_by(email=form.email.data).first()
		send_verification_mail(user)
		flash('An email has been sent', 'info')
		return redirect(url_for('home'))
	return render_template('auth_verification.html', title='Reset Password', form=form)
    


@app.route("/verify/<token>", methods=['GET', 'POST'])
def verify(token):
		passport =  User.verify_reset_token(token)
		if passport is None :
			flash('invalid or expired token', 'warning')		
		form = VerifyForm()
		if form.validate_on_submit():
			if(form.verification.data):	
				passport.verification = form.verification.data
				db.session.commit()
				flash('verfied successfully', 'success')
			if (passport.verification == 'VERIFIED'):
				send_mail(passport)
				return redirect(url_for('dashboard'))
			else:
				return "not verification uploaded", 400

		return render_template('verify.html', title = verify, form = form)


@app.route("/applicant/<token>")
def applicant(token):
		passport =  User.verify_reset_token(token)
		if passport is None :
			flash('invalid or expired token', 'warning')	

		return render_template('about_applicant.html',title='about_applicant', passport=passport)
	