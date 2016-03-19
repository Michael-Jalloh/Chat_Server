from peewee import *
from datetime import *
from passlib.apps import custom_app_context as PASSWORD
from itsdangerous import (TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired)


SECRET_KEY = 'This is my secret'

database = SqliteDatabase('test.db', **{})

class UnknownField(object):
	pass

class BaseModel(Model):
	class Meta:
		database = database

class User(BaseModel):
	
	username = CharField()
	password = CharField()
	email = CharField()
	joined_date = DateTimeField(default=datetime.utcnow)
	
	def hash_pass(self, password):
		self.password = PASSWORD.encrypt(password)
		
	
	def verify(self, password):
		return PASSWORD.verify(password, self.password)
		
	def generate_token(self, expiration=600):
		s = Serializer(SECRET_KEY, expires_in = expiration)
		return s.dumps({'id':self.id})
		
	
	@staticmethod
	def verify_token(token):
		s = Serializer(SECRET_KEY)
		try:
			data = s.loads(token)
		except SignatureExpired:
			return 'Expired Token'
		except BadSignature:
			return 'Invalid token'
		user = User.get(User.id == data['id'])
		return user
		
		
	
		
	class Meta:
		db_table = 'user'

class Post(BaseModel):
	body = TextField()
	sender = ForeignKeyField(User, related_name='smsg')
	receiver = ForeignKeyField(User,related_name='rmsg')
	timestamp = DateTimeField(default=datetime.utcnow)

	class Meta:
		db_table = 'post'
