# Copyright NYU-DevOps-Alpha team-customer. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
Customer Service

Paths:
------
GET /customers - Returns a list all of the customers
GET /customers/{id} - Returns the Customer with a given id number
POST /customers - creates a new Customer record in the database
PUT /customers/{id} - updates a Customer record in the database
DELETE /customers/{id} - deletes a Customer record in the database
"""

import os, re
import sys
import logging
from functools import wraps
from flask import Flask, jsonify, request, url_for, make_response
from flask_api import status    # HTTP Status Codes
from werkzeug.exceptions import NotFound, UnsupportedMediaType, BadRequest
from app.models import Customer, DataValidationError

from . import app

######################################################################
# Error Handlers
######################################################################
@app.errorhandler(DataValidationError)
def request_validation_error(error):
    """ Handles Value Errors from bad data """
    return bad_request(error)

@app.errorhandler(400)
def bad_request(error):
    """ Handles bad reuests with 400_BAD_REQUEST """
    message = error.message or str(error)
    app.logger.info(message)
    return jsonify(status=400, error='Bad Request', message=message), 400

@app.errorhandler(404)
def not_found(error):
    """ Handles resources not found with 404_NOT_FOUND """
    message = error.message or str(error)
    app.logger.info(message)
    return jsonify(status=404, error='Not Found', message=message), 404

@app.errorhandler(405)
def method_not_supported(error):
    """ Handles unsuppoted HTTP methods with 405_METHOD_NOT_SUPPORTED """
    message = error.message or str(error)
    app.logger.info(message)
    return jsonify(status=405, error='Method not Allowed', message=message), 405

@app.errorhandler(415)
def mediatype_not_supported(error):
	""" Handles unsuppoted media requests with 415_UNSUPPORTED_MEDIA_TYPE """
	message = error.message or str(error)
	app.logger.info(message)
	return jsonify(status=415, error='Unsupported media type', message=message), 415

@app.errorhandler(500)
def internal_server_error(error):
    """ Handles unexpected server error with 500_SERVER_ERROR """
    message = error.message or str(error)
    app.logger.info(message)
    return jsonify(status=500, error='Internal Server Error', message=message), 500

# check content type
def check_content_type(content_type):
    def decorater(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            """ Checks that the media type is correct """
            pattern = re.compile(content_type+'.*')
            if 'Content-Type' in request.headers:
                if pattern.match(request.headers['Content-Type']):
                    return f(*args, **kwargs)
                else:
                    app.logger.error('Invalid Content-Type: %s', request.headers['Content-Type'])
                    raise UnsupportedMediaType(' Content-Type must be {}'.format(content_type))
            else:
                # provide no content type
                app.logger.error('Provide No Content-Type')
                raise UnsupportedMediaType(' Content-Type must be {}'.format(content_type))
        return decorated_function
    return decorater

######################################################################
# GET INDEX
######################################################################
@app.route('/')
def index():
    """ Root URL response """
    return app.send_static_file('index.html')

######################################################################
# LIST ALL CUSTOMERS
######################################################################
@app.route('/customers', methods=['GET'])
def list_customers():
    """ Returns all of the Customers """
    customers = Customer.all()
    if not customers:
        raise NotFound("No Customers")
    results = [customer.serialize() for customer in customers]
    return make_response(jsonify(results), status.HTTP_200_OK)


######################################################################
# QUERY CUSTOMERS
######################################################################
@app.route('/customer', methods=['GET'])
@check_content_type('application/json')
def query_customers():
    """ Query parts of the Customers """
    customers = []
    last_name = request.args.get('lastname')
    first_name = request.args.get('firstname')
    if last_name:
        customers = Customer.find_by_lastname(last_name)
    elif first_name:
        customers = Customer.find_by_firstname(first_name)
    else:
        raise BadRequest("should provide firstname or lastname")
    if not customers:
        raise NotFound("No Customers Found")
    results = [customer.serialize() for customer in customers]
    return make_response(jsonify(results), status.HTTP_200_OK)

######################################################################
# RETRIEVE A CUSTOMER
######################################################################
@app.route('/customers/<int:customer_id>', methods=['GET'])
def get_customers(customer_id):
    """
    Retrieve a single Customer

    This endpoint will return a Customer based on it's id
    """
    customer = Customer.find(customer_id)
    if not customer:
        raise NotFound("Customer with id '{}' was not found.".format(customer_id))
    return make_response(jsonify(customer.serialize()), status.HTTP_200_OK)


######################################################################
# ADD A NEW CUSTOMER
######################################################################
@app.route('/customers', methods=['POST'])
@check_content_type('application/json')
def create_customers():
    """
    Add a Customer
    This endpoint will create a Customer based the data in the body that is posted
    """
    customer = Customer()
    customer.deserialize(request.get_json())
    customer.save()
    message = customer.serialize()
    location_url = url_for('get_customers', customer_id=customer.id, _external=True)
    return make_response(jsonify(message), status.HTTP_201_CREATED,
                         {
                             'Location': location_url
                         })


######################################################################
# UPDATE AN EXISTING CUSTOMER
######################################################################
@app.route('/customers/<int:customer_id>', methods=['PUT'])
@check_content_type('application/json')
def update_customers(customer_id):
    """
    Update a Customer

    This endpoint will update a Customer based the body that is posted
    """
    customer = Customer.find(customer_id)
    if not customer:
        raise NotFound("Customer with id '{}' was not found.".format(customer_id))
    customer.deserialize(request.get_json())
    customer.id = customer_id
    customer.save()
    return make_response(jsonify(customer.serialize()), status.HTTP_200_OK)


######################################################################
# DELETE A CUSTOMER
######################################################################
@app.route('/customers/<int:customer_id>', methods=['DELETE'])
@check_content_type('application/json')
def delete_customers(customer_id):
    """
    Delete a Customer

    This endpoint will delete a Customer based the id specified in the path
    """
    customer = Customer.find(customer_id)
    if customer:
        customer.delete()
    return make_response('', status.HTTP_204_NO_CONTENT)

######################################################################
#  U T I L I T Y   F U N C T I O N S
######################################################################

def initialize_logging(log_level):
    """ Initialized the default logging to STDOUT """
    if not app.debug:
        print 'Setting up logging...'
        # Set up default logging for submodules to use STDOUT
        # datefmt='%m/%d/%Y %I:%M:%S %p'
        fmt = '[%(asctime)s] %(levelname)s in %(module)s: %(message)s'
        logging.basicConfig(stream=sys.stdout, level=log_level, format=fmt)
        # Make a new log handler that uses STDOUT
        handler = logging.StreamHandler(sys.stdout)
        handler.setFormatter(logging.Formatter(fmt))
        handler.setLevel(log_level)
        # Remove the Flask default handlers and use our own
        handler_list = list(app.logger.handlers)
        for log_handler in handler_list:
            app.logger.removeHandler(log_handler)
        app.logger.addHandler(handler)
        app.logger.setLevel(log_level)
        app.logger.info('Logging handler established')
