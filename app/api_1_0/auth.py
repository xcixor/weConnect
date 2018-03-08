"""Contains view for authenticating the user"""

from flask import jsonify, request

from app.api_1_0 import api

from app.api_1_0.models import User

from app.api_1_0.errors import bad_request

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