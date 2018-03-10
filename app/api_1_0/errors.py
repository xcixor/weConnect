"""Contains custom errors for the api"""

from flask import jsonify

def bad_request(msg):
    """Server cannot process the request due to a client error
    Args:
        msg (str) Error message to display
    Returns:
        response: Error log
        status_code: 400   
    """
    response = jsonify({
        'error':'Bad request',
        'message':msg
    })
    response.status_code = 400
    return response

def forbidden(msg):
    """The user might not have the necessary permissions for a resource.
    Args:
        msg (str) Error message to display
    Returns:
        response: Error log
        status_code: 403 
    """
    response = jsonify({
        'error':'forbidden',
        'message':msg
    })
    response.status_code = 403
    return response

def unauthorized(msg):
    """Authentication is required and has failed or has not yet been provided.
    Args:
        msg (str) Error message to display
    Returns:
        response: Error log
        status_code: 401
    """
    response = jsonify({
        'error':'Unauthorized',
        'message':msg
    })
    response.status_code = 401
    return response

def not_found(msg):
    """The requested resource could not be found.
    Args:
        msg (str) Error message to display
    Returns:
        response: Error log
        status_code: 401
    """
    response = jsonify({
        'error':'Not Found',
        'message':msg
    })
    response.status_code = 404
    return response