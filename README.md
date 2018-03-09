[![Build Status](https://travis-ci.org/xcixor/weConnect.svg?branch=develop)](https://travis-ci.org/xcixor/weConnect)
[![Coverage Status](https://coveralls.io/repos/github/xcixor/weConnect/badge.svg?branch=develop)](https://coveralls.io/github/xcixor/weConnect?branch=develop)
[![Maintainability](https://api.codeclimate.com/v1/badges/19e2cda2bde6eac40512/maintainability)](https://codeclimate.com/github/xcixor/weConnect/maintainability)

### Prerequisites
    You should have the following software installed
        python3*
        virtualenv
### Installing
    Clone the project as follows:
    On the terminal for linux and mac, type: 
        $    git clone git@github.com:xcixor/weConnect.git
    This will download the project onto your machine locally
    After cloning navigate to the root folder and in the terminal create a virtual environment as follows:
        $    virtualenv 'preferred name of virtual environment'
    After creating the virtual environment, activate it as folllows:
        $    source 'your env'/bin/activate
    After activating the virtual environment, install the app's dependencies as follows:
        (myvenv) $    pip install -r requirements.txt
    Once the installed start the app as follows:
        (myvenv) $    python run.py runserver
    Navigate to the link provided by the server and start creating businesses!

## Running the Tests
    Run the test as follows:
        install nose first
        (myvenv) $ pip install nose
        (myvenv) $ nosetests tests/

# Mockups
[Uml](/designs/uml.png)

# Deployment
This app is hosted at github pages and you can access it
via this [link](https://xcixor.github.io/weConnect/)

# Built with
    Materialize framework 

# Contributing
    This app was peer reviewed by Patrick Migot and Eric Mwenda

# Versioning
    weConnect 1.0

# Licences
    None

