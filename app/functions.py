###############################################################################
# This is the file that will hold the functions that will be called in the    #
# Flask app. It will handle all the interaction between the database and the  #
# web app...                                                                  #
###############################################################################

from models import *

class USER:
	username = ''
	id = ''
	

class POST:
	body = ''
	id = ''
	sender = ''


def verifier(id_or_token, password):
	try:
		user = User.verify_token(id_or_token)

		if not type(user) == User:
			try:
				user = User.get(User.id == id_or_token)
				if not user.verify(password):
					return False
			except User.DoesNotExist:
				return False
		u = USER()
		u.username = user.username
		u.id = user.id
		return u
	except:
		return False 


def get_token(user):
	token = User.get(User.id == user.id).generate_token()
	return token		

def get_msg(user):
	msg = []
	msg = User.get(User.id == user.id).rmsg
	return msg

def name_change(user, username):
	try:
		m = User.get(User.id == user.id)
		m.username = username
		m.save()
		return m.username 	
	except User.DoesNotExist:
		return False

def get_email(user):
	try:
		m = User.get(User.id == user.id)
		email = m.email
		return email
	except User.DoesNotExist:
		return False

def email_change(user, email):
	try:
		m = User.get(User.id == user.id)
		m.email = email
		return email
	except User.DoesNotExist:
		return False
