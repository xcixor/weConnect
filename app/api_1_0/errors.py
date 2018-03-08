"""Contains custom errors for the api"""
from flask import jsonify

def bad_request(msg):
    response = jsonify({
        'error':'Bad request',
        'message':msg
    })
    response.status_code = 400
    return response

def forbidden(msg):
    response = jsonify({
        'error':'forbidden',
        'message':msg
    })
    response.status_code = 403
    return response

def unauthorized(msg):
    response = jsonify({
        'error':'Unauthorized',
        'message':msg
    })
    response.status_code = 401
    return response

def not_found(msg):
    response = jsonify({
        'error':'Not Found',
        'message':msg
    })
    response.status_code = 404
    return response