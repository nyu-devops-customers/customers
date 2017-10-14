# Copyright 2016, 2017 John J. Rofrano. All Rights Reserved.
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
Customer Shop Demo

This is an example of a shop service written with Python Flask
It demonstraits how a RESTful service should be implemented.

Paths
-----
GET  /customers - Retrieves a list of customers from the database
GET  /customers{id} - Retrirves a Customer with a specific id
POST /customers - Creates a Customer in the datbase from the posted database
PUT  /customers/{id} - Updates a Customer in the database fom the posted database
DELETE /customers{id} - Removes a Customer from the database that matches the id
"""
import sys
import os
import logging
from flask import Flask, Response, jsonify, request, json, url_for, make_response
from models import Customer, DataValidationError
#from flask_api import status    # HTTP Status Codes

# Pull options from environment
DEBUG = (os.getenv('DEBUG', 'False') == 'True')
PORT = os.getenv('PORT', '5000')
HOST = os.getenv('HOST','0.0.0.0')

# Create Flask application
app = Flask(__name__)

# Status Codes
HTTP_200_OK = 200
HTTP_201_CREATED = 201
HTTP_204_NO_CONTENT = 204
HTTP_400_BAD_REQUEST = 400
HTTP_404_NOT_FOUND = 404
HTTP_409_CONFLICT = 409

######################################################################
# Error Handlers
######################################################################
@app.errorhandler(DataValidationError)
def request_validation_error(error):
    """ Handles all data validation issues from the model """
    return bad_request(error)

@app.errorhandler(400)
def bad_request(error):
    """ Handles requests that have bad or malformed data """
    return jsonify(status=400, error='Bad Request', message=error.message), 400

@app.errorhandler(404)
def not_found(error):
    """ Handles Customers that cannot be found """
    return jsonify(status=404, error='Not Found', message=error.message), 404

@app.errorhandler(405)
def method_not_supported(error):
    """ Handles bad method calls """
    return jsonify(status=405, error='Method not Allowed',
                   message='Your request method is not supported.' \
                   ' Check your HTTP method and try again.'), 405

@app.errorhandler(500)
def internal_server_error(error):
    """ Handles catostrophic errors """
    return jsonify(status=500, error='Internal Server Error', message=error.message), 500


######################################################################
# GET INDEX
######################################################################
@app.route('/')
def index():
    """ Return something useful by default """
    return jsonify(name='Customer Demo REST API Service',
                   version='1.0',
                   url=url_for('list_customers', _external=True)), HTTP_200_OK

######################################################################
# LIST ALL CustomerS
######################################################################
@app.route('/customers', methods=['GET'])
def list_customers():
    """ Retrieves a list of customers from the database """
    results = []
    lastname = request.args.get('lastname')
    if lastname:
        results = Customer.find_by_lastname(lastname)
    else:
        results = Customer.all()

    return jsonify([customer.serialize() for customer in results]), HTTP_200_OK

######################################################################
# RETRIEVE A Customer
######################################################################
@app.route('/customers/<int:id>', methods=['GET'])
def get_customers(id):
    """ Retrieves a Customer with a specific id """
    customer = Customer.find(id)
    if customer:
        message = customer.serialize()
        return_code = HTTP_200_OK
    else:
        message = {'error' : 'Customer with id: %s was not found' % str(id)}
        return_code = HTTP_404_NOT_FOUND

    return jsonify(message), return_code

######################################################################
# ADD A NEW Customer
######################################################################
@app.route('/customers', methods=['POST'])
def create_customers():
    """ Creates a Customer in the datbase from the posted database """
    payload = request.get_json()
    customer = Customer()
    customer.deserialize(payload)
    customer.save()
    message = customer.serialize()
    response = make_response(jsonify(message), HTTP_201_CREATED)
    response.headers['Location'] = url_for('get_customers', id=customer.id, _external=True)
    return response

######################################################################
# UPDATE AN EXISTING Customer
######################################################################
@app.route('/customers/<int:id>', methods=['PUT'])
def update_customers(id):
    """ Updates a Customer in the database fom the posted database """
    customer = Customer.find(id)
    if customer:
        payload = request.get_json()
        customer.deserialize(payload)
        customer.save()
        message = customer.serialize()
        return_code = HTTP_200_OK
    else:
        message = {'error' : 'Customer with id: %s was not found' % str(id)}
        return_code = HTTP_404_NOT_FOUND

    return jsonify(message), return_code

######################################################################
# DELETE A Customer
######################################################################
@app.route('/customers/<int:id>', methods=['DELETE'])
def delete_customers(id):
    """ Removes a Customer from the database that matches the id """
    customer = Customer.find(id)
    if customer:
        customer.delete()
    return make_response('', HTTP_204_NO_CONTENT)
######################################################################
#  U T I L I T Y   F U N C T I O N S
######################################################################
'''
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
'''
######################################################################
#   M A I N
######################################################################
if __name__ == "__main__":
    # dummy data for testing
#    print "Customer Service Starting..."
   # initialize_logging(logging.INFO)   
    app.run(host='0.0.0.0', port=int(PORT), debug=DEBUG)
