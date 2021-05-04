from datetime import datetime
from flask_app import db, app, login_manager
from flask_login import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as serializer

@login_manager.user_loader
def load_user(user_id):
		return User.query.get(int(user_id))


class User(db.Model, UserMixin):
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(20), unique=True, nullable=False)
	email = db.Column(db.String(120), unique=True, nullable=False)
	image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
	password = db.Column(db.String(60), nullable=False)

	def get_reset_token(self, expires_sec=1800):
		s = serializer(app.config['SECRET_KEY'],expires_sec)
		return s.dumps({'user_id':self.id}).decode('utf-8')


	@staticmethod
	def verify_reset_token(token):
		s = serializer(app.config['SECRET_KEY'])

		try:
			user_id = s.loads(token)['user_id']
		except:
			return None
		return Passport.query.get(user_id)

	

	passports = db.relationship('Passport', backref='author', lazy=True)


	def __repr__(self):
		return f"User('{self.username}', '{self.email}', '{self.image_file}', '{self.password}')"

class Passport(db.Model):
	id = db.Column(db.Integer, primary_key=True)

	name = db.Column(db.String(20), nullable=False)

	email = db.Column(db.String(120), unique=True, nullable=False)

	passport_picture = db.Column(db.String(20), nullable=False)

	date_of_birth = db.Column(db.String(20), nullable=False)

	phone = db.Column(db.Integer, nullable=False)

	address = db.Column(db.Text, nullable=False)

	verification = db.Column(db.String(60), nullable=False, default='notverified')

	date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
	

	user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

	def get_reset_token(self, expires_sec=1800):
		s = serializer(app.config['SECRET_KEY'],expires_sec)
		return s.dumps({'user_id':self.id}).decode('utf-8')

	@staticmethod
	def verify_reset_token(token):
		s = serializer(app.config['SECRET_KEY'])

		try:
			user_id = s.loads(token)['user_id']
		except:
			return None
		return Passport.query.get(user_id)




	def __repr__(self):
		return f"Passport('{self.name}', '{self.email}', '{self.passport_picture}', '{self.date_of_birth}', '{self.date_posted}','{self.verification}')"

