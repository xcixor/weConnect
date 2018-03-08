"""Contains view for authenticating the user"""

from flask import jsonify, request, current_app

from app.api_1_0 import api

from app.api_1_0.models import User

from app.api_1_0.errors import bad_request, forbidden, unauthorized

import jwt

from datetime import datetime, timedelta

from functools import wraps

black_list = []

@api.route('/auth/register', methods=['POST'])
def register_user():
    """Register new user"""
    username = str(request.data.get('Username', ''))
    email = str(request.data.get('Email', ''))
    password = str(request.data.get('Password', ''))
    confirm_password = str(request.data.get('Confirm Password', ''))
    if username and email and password and confirm_password:
        user = User(username, email, password, confirm_password)
        user_created = user.register_user()
        if user_created == True:      
            response = jsonify({
                "Message":"{} has successfuly created an account"\
                .format(user.name)              
            })
            response.status_code = 201
            return response
        else:
            return bad_request(user_created)    
    else:
        return bad_request("Some data fields are missing")

@api.route('/auth/login', methods=['POST'])
def login():
    """Log a user into their account"""
    username = str(request.data.get('Username', ''))
    password = str(request.data.get('Password', ''))
    if username and password:
        if User.login(username, password):
            # generate  token to manage user's session
            token = jwt.encode({
                'id':username,
                'exp': datetime.utcnow() + timedelta(minutes=30)},
                current_app.config.get('SECRET_KEY')
            )
            if token:
                response = jsonify({
                    'token': token.decode('UTF-8'),
                    "Message":"{} has successfuly logged in"\
                    .format(username)              
                })
                response.status_code = 200
                return response
        else:
            return forbidden("Invalid username/password combination")
    else:
        return bad_request("Please provide all the fields")

def auth_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        # verify token
        token = None
        #check if x-access-token which is used to store the token is in headers
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']
        if not token:
            return unauthorized('Token missing')
        try:
            data = jwt.decode(token, current_app.config.get('SECRET_KEY'))
            current_user = User.get_user(data['id'])
        if token in black_list:
            return unauthorized('You need to login!')
        except:
            return unauthorized('Token is invalid')
        return f(current_user, *args, **kwargs)
    return decorated

@api.route('/auth/reset-password', methods=['POST'])
@auth_required
def reset_password(current_user):
    """Resets user password"""
    if not current_user:
        return unauthorized('You are not allowed to perform this action')
    username = str(request.data.get('Username', ''))
    old_password = str(request.data.get('Previous Password', ''))
    new_password = str(request.data.get('New Password', ''))
    if username and old_password and new_password:
        update_user = User.reset_password(username, old_password, new_password)
        if update_user:
            response = jsonify({
                "Message":"Successfuly changed password"
            })
            response.status_code = 200
            return response
        else:
            return forbidden(update_user)
    else:
        return bad_request("Provide all fields")

    @api.route('/auth/logout', methods=['POST'])
    @auth_required
    def log_out(current_user):
        if not current_user:
            return unauthorized('You are not allowed to perform this action')
        token = request.headers['x-access-token']
        black_list.append(token)
        response = jsonify{
            'message'='Logged out'
        }
        response.status_code = 201
        return response

        

