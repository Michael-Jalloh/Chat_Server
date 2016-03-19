from flask import Flask, request, make_response, jsonify, abort, g 
from flask.ext.restful import Api, Resource
from flask.ext.httpauth import HTTPBasicAuth
from app.models import *
from app import functions
from OpenSSL import SSL
 

context = SSL.Context(SSL.SSLv3_METHOD)
context.use_privatekey_file('server.key')
context.use_certificate_file('server.crt')

app = Flask(__name__)
app.config.from_object('config')
api = Api(app)
auth = HTTPBasicAuth()



class BaseAPI(Resource):

	
	@app.before_request
	def before_request():
		print 'Before request'

		
	@app.after_request
	def after_request(response):
		print 'After request'
		return response

		
	@app.errorhandler(404)
	def not_found(error):
		return make_response(jsonify({'error':'Not found'}), 404)
	



	@auth.verify_password
	def verify_password(id_or_token, password):
		user = functions.verifier(id_or_token, password)
		if user == False:
			return False
		
		g.user = user
		return True

	@auth.error_handler
	def unauthorized():
		return make_response(jsonify({'error':'Unauthorized access'}), 401)


class UserAPI(BaseAPI):

	@auth.login_required
	def get(self):
		service = request.json['serive']
		reply = 'reply'
		if service == 'msg':
			msg = functions.get_msg(g.user)
			return  make_response(jsonify({reply:msg}))
		elif service == 'get_name':
			name = g.user.username
			return make_response(jsonify({reply:name}))
		elif service == 'email':
			email = functions.get_email(g.user)
			return make_response(jsonify({reply:email}))

		


	@auth.login_required		
	def post(self):
		t = functions.get_token(g.user)	
		return make_response(jsonify({'token':t}))

	@auth.login_required
	def put(self):
		service = request.json['service']
		if service == 'username':
			username = request.json['username']
			username = functions.name_change(g.user, username)
			if not username:
				return False
			user = {}
			user['id'] = g.user.id
			user['username'] = username
			return make_response(jsonify(user))

		elif service == 'email':
			email = request.json['email']
			email = functions.email_change(user, email)
			if not email:
				return False
			user = {}
			user['id'] = g.user.id
			user['username'] = g,user.username
			user['email'] = email
			return make_response(jsonify(user))

	@auth.login_required
	def delete(self):
		return 'This is the DELETE method'
		

api.add_resource(UserAPI,'/users', endpoint='user')

if __name__=='__main__':
	app.run(debug=True)
