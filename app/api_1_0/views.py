"""Contains view for authenticating the user"""

from flask import jsonify, request, current_app

from app.api_1_0 import api

from app.api_1_0.models import User, Business

from app.api_1_0.errors import bad_request, forbidden, unauthorized, not_found

import jwt

from datetime import datetime, timedelta

from functools import wraps

black_list = []

business_list = []

current_user = {}

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
        except:
            return unauthorized('Token is invalid')
        if token in black_list:
            return unauthorized('You need to login!')

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
    response = jsonify({
        'message':'Logged out'
    })
    response.status_code = 201
    return response

@api.route('/businesses', methods=['POST'])
@auth_required
def create_business(current_user):
    """"""
    name = str(request.data.get('Name', ''))
    description = str(request.data.get('Description', ''))
    category = str(request.data.get('Category', ''))
    location = str(request.data.get('Location', ''))
    address = str(request.data.get('Address', ''))
    
    if name and description and category and location and address:
        business = Business(name, description, category, location, address, current_user['Username'])
        status = business.create_business(business_list)
        if status:
            response = jsonify(status)
            response.status_code = 201
            return response
        else:
            bad_request(status)
    else:
        return forbidden('Required fields are missing')
@api.route('/businesses', methods=['GET'])
def retrieve_businesses():
    businesses = business_list
    if businesses:
        response =jsonify(businesses)
        response.status_code = 200
        return response
    else:
        return not_found("There are no businesss in our database")
        
@api.route('/businesses/<int:bid>', methods=['GET', 'PUT', 'DELETE'])
@auth_required
def manipulate_business(current_user, bid, **kwargs):
    # if type(bid) != int:
    #     return bad_request("Wrong data type")
    
    #get business by id
    business_found = Business.get_business_by_id(business_list, bid)
    if not business_found:
        return not_found('That business was not found in our server please check again later')
    business = Business(business_found['Name'], business_found['Description'], business_found['Category'], business_found['Location'], business_found['Address'], business_found['Owner'])
    if request.method == 'DELETE':
        Business.delete_business(business_list, bid)
        return{
            'Message': "business {} has been successfully deleted".format(business_found['Name'])
        }, 200
    elif request.method == 'GET':
        response = jsonify(business_found)
        response.status_code = 200
        return response
    else:
        # update business
        name = str(request.data.get('Name', ''))
        description = str(request.data.get('Description', ''))
        category = str(request.data.get('Category', ''))
        location = str(request.data.get('Location', ''))
        address = str(request.data.get('Address', ''))
        
        keys = {}
        if name:
            keys['Name'] = name
        if location:
            keys['Location'] = location
        if category:
            keys['Category'] = category
        if description:
            keys['Description'] = description
        if address:
            keys['Address'] = address
        for key, value in keys.items():
            kwargs = {key:value}            
        status = business.edit_business(business_list, **kwargs)  
        if status:
            response = jsonify({"message":"Business edited successfuly"})
            response.status_code = 200
            return response
        not_found("That business does not exist in our db")

@api.route('/businesses/<int:bid>/reviews', methods=['POST', 'GET'])
def business_reviews(bid):
    business_found = Business.get_business_by_id(business_list, bid)
    if not business_found:
        return not_found('That business was not found in our server please check again later') 
    business = Business(business_found['Name'], business_found['Description'], business_found['Category'], business_found['Location'], business_found['Address'], business_found['Owner'])
    if request.method == 'POST':   
        name = str(request.data.get('Email', ''))
        comment = str(request.data.get('Comment', ''))
        if name and comment:
            business.write_review(business_list, comment, name)
            response = jsonify({
                "message":"success"
            })
            response.status_code = 200
            return response
        else:
            return bad_request("Invalid data provided")
    else:
        # get reviews
        reviews = business_found['Reviews']
        if reviews:
            response = jsonify({
                "Reviews":business_found['Reviews']
            })
            response.status_code = 200
            return response
        else:
            response = jsonify({
                "message":"No reviews for this business"
            })
            response.status_code = 404
            return response