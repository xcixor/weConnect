"""Contains classes for modelling the app"""
import re

class User(object):
    """Defines an application user
    
    Attributes:

    methods

    create_account(), login(), log_out(), reset_password(), 
    validate_email(), find_user()
    """

    def __init__(self, username, email, password, confirm_password):
        """Initializes the app
        
        Args:

        name(str) - User's name
        email(str) - Users email address
        password(str) - Authentication password
        confirm_password(str) - Confirmation password
        login_status(bool) - True if the user is logged in
        """
        self.name = username
        self.email = email
        self. password = password
        self.confirm_password = confirm_password
        self.login_status = False
        
    def find_user(self, user_list):
        """Checks whether a user exists in the users list
        
        Returns:

        True if user is in the users list, False otherwise
        """
        registered_user = [user for user in user_list if user['Username'].lower() \
        == self.name.lower()]
        if registered_user:
            return True
        return False

    def register_user(self, user_list):
        """Creates user account
        
        Returns:
            {
                True: if user is registered successfuly,
                message: to give reason for registration failure
            }
        

        """
        if self.find_user(user_list):
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
            user = {'Username':self.name, 'Email':self.email,
            'Password':self.password}
            user_list.append(user)
            return True

    @staticmethod
    def verify_password_length(password):
        """Check password is valid
        
        Returns:

        True if password is long enough
        """
        if (len(password)) >= 6:
            return True

    @staticmethod
    def verify_username(username):
        """Check password is valid
        
        Returns:

        True if username is valid
        """
        if re.match("^[a-zA-Z0-9_]*$", username):
            return True

    @staticmethod
    def verify_email(email):
        """Check if email is valid
        
        Returns:

        True if email is valid
        """
        if re.match(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)", 
            email):
            return True
    @classmethod
    def login(cls, user_list,username, password):
        """Logs a user into his account
        
        Returns:

        True if user is successfuly logged in
        """
        loging_user = [user for user in user_list if user['Username'] \
        == username]
        if loging_user and loging_user[0]['Password'] == password:
            return True
    @classmethod       
    def reset_password(cls, user_list, username, old_password, new_password):
        """Resets a user's password

        Returns:

        message: To tell the status of the change
        """
        user_to_update = [user for user in user_list if user['Username'] \
        == username]
        if user_to_update:
            if old_password == user_to_update[0]['Password']: 
                if User.verify_password_length(new_password):
                    user_to_update[0]['Password'] = new_password
                    return {'message':'Password successfully changed'}
                else:
                    return {"message":"Password cannot be less than \
                    6 characters!"}
            else:
                return {"message":"Previous password incorrect"}
        else:
            return {"message":"That user does not exist"}

    def log_out(self):
        """Logs a user out of the account

        Returns:

        True if success
        """
        self.login_status = False
        return True

    @classmethod
    def get_user(cls, user_list, username):
        """Retrieves a user for the users list

        Returns:

        user: dictionary containing user's details
        """
        user = [user for user in user_list if user['Username'] == username]
        return user[0]

    @classmethod
    def get_users(cls, user_list):
        """Retrieves all users from the users list
        
        Returns:

        users: List containing all the app users
        """
        return user_list

class Review(object):
    """Defines a review

    Methods:

    create_review(), delete_review(), validate_comment()
    """

    def __init__(self, description, owner):
        """Initializes a review object
        
        Args:
        {
            description: comment description,
            owner: The user who has commented
            }
        """
        self.description = description
        self.owner = owner
        
    def create_review(self):
        """Adds a review to a reviews list

        Args:

        reviews(list) - Where reviews are stored

        Returns:

        message: to display creation status         
        """
        # Review.count += 1
        review = {'Comment':self.description, 'Owner':self.owner}
        return review

class Business(object):
    """Defines a business

    Methods:

    create_business(), view_business(), 
    update_business(), delete_business(), write_review(), get_all_reviews()
    """
    
    def __init__(self, name, description, category, location, address, \
        owner):
        """Initializes a business object

        Args:
        {
            businesses(list) - record a business created, 
            name(str) - the name of the business, 
            description(str) - a description of the business, 
            category(str) - business' categorization, 
            location(str) - the business' situation, 
            comments(list) - customer opinions about the business
        }        
        """
        self.name = name
        self.description = description
        self.category = category
        self.location = location
        self.address = address
        self.owner = owner
        self.reviews = []

    def create_business(self, business_list):
        """Creates a business dictionary from the business attributes \
        and stores them in a list

        Args:
        
        business_list: stores the business dict

        Returns:
        
        message: to show the creation status
        """
        if self.find_business(business_list):
            return {"message":"Cannot create duplicate business"}
        else:
            business_id = self.generate_id(business_list)  
            business = {'Id':business_id, "Owner":self.owner, 'Name': self.name, 
            'Description':self.description, \
            'Category':self.category, 'Location':self.location, 
            'Reviews':self.reviews, 'Address':self.address}
            business_list.append(business)
            return {"message":"{} successfuly created".format(self.name)}
    def generate_id(self, business_list, business_id=0):
        """Generates a business id to uniquely identify a business

        Args:
            {
                business_list(list) - where other businesses have been stored,
                business_id(int) - an integer initialized to zero at the beginining of execution
            }
        

        returns:
        business_id: a unique identifier for the business
        """
        if business_id == 0:
            business_id = len(business_list) + 1
        for business in business_list:
            if business['Id'] == business_id:
                business_id += 1
                self.generate_id(business_list, business_id)
        return business_id


    @classmethod
    def get_all_businesses(cls, business_list):
        """Generates a list of all the businesses created

        Args:

        business_list(list) The list where the businesses are stored
        
        Returns:

        business_list: A list of all the businesses created
        """
        return business_list

    def find_business(self, business_list):
        """Checks whether a business exists in a list
        
        Args:

        business_list(list) - The list to iterate over

        Returns:{
            business: A dictionary containing the found business,
            None: If the business is not found
        }
        """
        found_business = [business for business in business_list if \
        business['Name'].lower() == self.name.lower()]
        if found_business:
            return found_business[0]
        else:
            return None

    def edit_business(self,business_list, **kwargs):
        """Edits the details of a business
        
        Args:{
            business_list - Where the business to edit is located,
            keyword arguments - The Fields of the business to change
        }

        Returns:

        False if the business could not be edited
        """
        category_to_update = self.find_business(business_list)
        if category_to_update:
            for key, value in kwargs.items():
                category_to_update [key] = value
        return False
                
    @classmethod
    def delete_business(cls, business_list, id):
        """Deletes a business
        
        Args:{
            business_list: Where the business is located
            id - A unique identifier of the business
        }
        Returns:{
            bool:
                True if deletion successful
                False if deletion not successful
        }
        """
        found_business = Business.get_business_by_id(business_list, id)
        if found_business:
            business_list.remove(found_business)
            return True
        else:
            return False

    @classmethod
    def get_business_by_id(cls, business_list, business_id):
        """Searches for a business by id
        Args:{
            business_list: Where the business is located
            id - A unique identifier of the business
        }

        Returns:

        found_business: A dictionary containing the business
        """
        print(business_list)
        found_business = [business for business in business_list if business['Id'] \
        == business_id]
        if len(found_business)>0:
            return found_business[0]
        

    @classmethod
    def get_businesses_by_category(cls, business_list, category):
        """Searches for all the business in a particular category

        Args:{
            business_list: A list of all the businesses,
            category: The category to search for
        }

        Returns:

        found_business: A list of all the businesses in that category
        """
        found_businesses = [business for business in business_list if \
        business['Category'].lower() == category.lower()]
        return found_businesses

    @classmethod
    def get_businesses_by_location(cls, business_list, location):
        """Searches for all the business in a particular location

        Args:{
            business_list: A list of all the businesses,
            location: The location to search for
        }

        Returns:

        found_business: A list of all the businesses in that location
        """
        found_businesses = [business for business in business_list if \
        business['Location'] == location]
        return found_businesses

    def write_review(self, business_list, comment, owner):
        """Writes a review for the business

        Args:{
            business_list: Record of all the businesses,
            comment: The comment about the business
            owner: The author of the comment
        }

        Returns:

        message: to display the status of execution
        
        """
        update_business = self.find_business(business_list)
        if update_business:
            review = Review(comment, owner)
            created_review = review.create_review()
            update_business['Reviews'].append(created_review)
            return {'message': 'Review written sucessfuly'}            


    def get_all_reviews(self):
        """Retrieves all the reviews for a business
        
        Returns:
        
        reviews: a list of all the reviews
        """
        return self.reviews








    
