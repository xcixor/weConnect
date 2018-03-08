"""Contains view for authenticating the user"""

from flask import jsonify, request, current_app

from app.api_1_0 import api

from app.api_1_0.models import User

from app.api_1_0.errors import bad_request, forbidden

import jwt

from datetime import datetime, timedelta

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