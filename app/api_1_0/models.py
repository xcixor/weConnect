"""Contains classes for modelling the app"""
import re

import json
class User(object):
    """Defines an application user
    Attributes:

    users(list) - a list of application users
    name(str) - User's name
    email(str) - Users email address
    password(str) - Authentication password

    methods

    create_account(), login(), log_out(), reset_password(), 
    validate_email(), find_user(), 
    """
    users = []

    def __init__(self, username, email, password, confirm_password):
        self.name = username
        self.email = email
        self. password = password
        self.confirm_password = confirm_password
        self.login_status = False
        
    def find_user(self):
        """Checks whether a user exists in the users list"""
        registered_user = [user for user in User.users if user['Username'].lower() == self.name.lower()]
        if registered_user:
            return True
        return False

    def register_user(self):
        """Creates user account"""
        if self.find_user():
            return {"message":"User already exist!"}
        elif not self.verify_password_length(self.password):
            return {"message":"Password cannot be less than 6 characters!"}
        elif self.password != self.confirm_password:
            return {"message":"Passwords don't match!"}
        elif not self.verify_username(self.name):
            return {"message":"Username cannot contain special characters" } 
        elif not self.verify_email(self.email):
            return {"message":"Invalid email address!"}
        else:
            user = {'Username':self.name, 'Email':self.email, 'Password':self.password}
            User.users.append(user)
            return True

    @staticmethod
    def verify_password_length(password):
        """Check password is valid"""
        if (len(password)) >= 6:
            return True

    @staticmethod
    def verify_username(username):
        """Check password is valid"""
        if re.match("^[a-zA-Z0-9_]*$", username):
            return True

    @staticmethod
    def verify_email(email):
        """Check if email is valid"""
        if re.match(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)", email):
            return True
    @classmethod
    def login(cls, username, password):
        """Logs a user into his account"""
        loging_user = [user for user in User.users if user['Username'] == username]
        if loging_user and loging_user[0]['Password'] == password:
            return True
    @classmethod       
    def reset_password(cls, username, old_password, new_password):
        user_to_update = [user for user in User.users if user['Username'] == username]
        if user_to_update:
            if old_password == user_to_update[0]['Password']: 
                if User.verify_password_length(new_password):
                    user_to_update[0]['Password'] = new_password
                    return {'message':'Password successfully changed'}
                else:
                    return {"message":"Password cannot be less than 6 characters!"}
            else:
                return {"message":"Previous password incorrect"}
        else:
            return {"message":"That user does not exist"}

    def log_out(self):
        self.login_status = True
        return True

    @classmethod
    def get_user(cls, username):
        user = [user for user in User.users if user['Username'] == username]        
        return user[0]

    @classmethod
    def get_users(cls):
        return User.users

class Business(object):
    """Defines a business
    
    Attributes:
    
    businesses(List), name(str), description(str), 
    category(str), location(str), comments(list)

    Methods:

    create_business(), view_business(), 
    update_business(), delete_business(), write_review(), get_all_reviews()
    """
    
    def __init__(self, name, description, category, location, address, owner):
        self.name = name
        self.description = description
        self.category = category
        self.location = location
        self.address = address
        self.owner = owner
        self.reviews = []

    def create_business(self, business_list):
        if self.find_business(business_list):
            return {"message":"Cannot create duplicate business"}
        else:         
            bid = self.generate_id(business_list)  
            business = {'Id':bid, "Owner":self.owner, 'Name': self.name, 'Description':self.description, \
            'Category':self.category, 'Location':self.location, 'Reviews':self.reviews, 'Address':self.address}
            business_list.append(business)
            return True
    def generate_id(self, business_list, bid=0):
        # print(json.dump(business_list))
        if bid == 0:
            bid = len(business_list) + 1
        for business in business_list:
            if business['Id'] == bid:
                bid += 1
                self.generate_id(business_list, bid)
        return bid


    @classmethod
    def get_all_businesses(cls, business_list):
        return business_list

    def find_business(self, business_list):
        found_business = [business for business in business_list if business['Name'].lower() == self.name.lower()]
        if found_business:
            return found_business[0]
        else:
            return None

    def edit_business(self,business_list, **kwargs):
        category_to_update = self.find_business(business_list)
        if category_to_update:
            for key, value in kwargs.items():
                category_to_update [key] = value
                
    @classmethod
    def delete_business(cls, business_list, id):
        found_business = Business.get_business_by_id(business_list, id)
        if found_business:
            business_list.remove(found_business)
            return True
        else:
            return False

    @classmethod
    def get_business_by_id(cls, business_list, bid):
        print(business_list)
        found_business = [business for business in business_list if business['Id'] == bid]
        if len(found_business)>0:
            return found_business[0]
        return {"message":"not found"}

    @classmethod
    def get_businesses_by_category(cls, business_list, category):
        found_businesses = [business for business in business_list if business['Category'].lower() == category.lower()]
        return found_businesses

    @classmethod
    def get_businesses_by_location(cls, business_list, location):
        found_businesses = [business for business in business_list if business['Location'] == location]
        return found_businesses

    def write_review(self, business_list, description, owner):
        business_to_update = self.find_business(business_list) 
        review = Review(description, owner)   
        business_review = review.create_review()     
        business_to_update ['Reviews'].append(business_review) 
        # business_review = review.create_review()
        # if business_review:
        #     self.reviews.append(business_review)
        #     return {'message':'Review written successfuly'}

    def get_all_reviews(self):
        return self.reviews

class Review(object):
    """Defines a review
    
    Attributes:

    description(str), owner(str)

    Methods:

    create_review(), delete_review(), validate_comment()
    """

    def __init__(self, description, owner):
        self.description = description
        self.owner = owner

    def create_review(self):
        # Review.count += 1
        review = {'Comment':self.description, 'Owner':self.owner}
        return {'message':'Review written successfuly'}


  






    
