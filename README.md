[![Build Status](https://travis-ci.org/xcixor/weConnect.svg?branch=develop)](https://travis-ci.org/xcixor/weConnect)
[![Coverage Status](https://coveralls.io/repos/github/xcixor/weConnect/badge.svg?branch=develop)](https://coveralls.io/github/xcixor/weConnect?branch=develop)
[![Maintainability](https://api.codeclimate.com/v1/badges/19e2cda2bde6eac40512/maintainability)](https://codeclimate.com/github/xcixor/weConnect/maintainability)

### we_connect
    This platform provides business owners a means to present their
    businesses to their customers and other businessmen. Customers can in turn comment
    about their experience on the services offered by the business.


### Prerequisites
    You should have the following software installed
        python3*
        preferred virtual environment creation tool
### Installing
    Clone the project as follows:
    On the terminal for linux and mac, type:
        $    git clone git@github.com:xcixor/weConnect.git
    This will download the project onto your machine locally
    After cloning navigate to the root folder and in the terminal create a virtual environment.
    For example if using virtual environment do the following:
        $    virtualenv 'preferred name of virtual environment'
    After creating the virtual environment, activate it as folllows:
        $    source 'your env'/bin/activate
    After activating the virtual environment, install the app's dependencies as follows:
        (myvenv) $    pip install -r requirements.txt
    Once the installed start the app as follows:
        (myvenv) $    python run.py runserver

## Running the Tests
    Run the test as follows:
        install nose first
        (myvenv) $ pip install nose
        Ensure you are in the root folder and run the following command
        (myvenv) $ nosetests tests/

## API endpoints
|Resource urls                                    | Method     | Description               | Requires token  |
|-------------------------------------------------|------------|---------------------------|-----------------|
| /api/v1/auth/register                           |   POST     | Register a user           |    FALSE        |
| /api/v1/auth/login                              |   POST     | Login user                |    FALSE        |
| /api/v1/auth/reset-password                     |   POST     | Rest user password        |    TRUE         |
| /api/v1/businesses                              |   POST     | Create business           |    TRUE         |
| /api/v1/businesses/&lt;business_id&gt;          |   PUT      | Update business profile   |    TRUE         |
| /api/v1/businesses/&lt;business_id&gt;          |   DELETE   | Remove a business         |    TRUE         |
| /api/v1/businesses                              |   GET      | Retrieve businesses       |    FALSE        |
| /api/v1/businesses/&lt;business_id&gt;          |   GET      | Retrieve a business       |    TRUE         |
| /api/v1/businesses/&lt;business_id&gt;/reviews  |   POST     | Add review for a business |    FALSE        |
| /api/v1/businesses/&lt;business_id&gt;/reviews  |   GET      | Retrieve business reviews |    FALSE        |

## Documentation
The documentation for the api can found [here](https://weconnect5.docs.apiary.io/#)
## Testing the api
    To test the above endpoints you need to have a tool like postman or Insomnia REST Client.
    Make requests to the api endpoints above to build and manage businesses

# Mockups
[Uml](/designs/uml.png)

# Deployment
The app is hosted at heroku
The fronted is demonstrated at github pages and you can access it
via this [link](https://xcixor.github.io/weConnect/)

# Built with
    FlaskAPI
    Materialize framework

# Contributing
    This app was peer reviewed by Patrick Migot, Cosmas28, Clifford254 and Eric Mwenda

# Versioning
    weConnect 1.0

# Licences
    None
