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
PUT /customers/{id}/upgrade-credit - updates a Customer credit_level record in the database
PUT /customers/{id}/downgrade-credit - updates a Customer credit_level record in the database
"""

import os, sys
import re
import logging
from functools import wraps
from flask import jsonify, request, json, url_for, make_response, abort
from flask_api import status    # HTTP Status Codes
from flask_restplus import Api as  BaseApi, Resource, fields
from werkzeug.exceptions import NotFound
from werkzeug.exceptions import NotFound, UnsupportedMediaType, BadRequest
from app.models import Customer, DataValidationError, DatabaseConnectionError

from . import app

from nose.tools import set_trace

# Overwirte the original implementation to enable using the '/' as root
# from github flask-restplus/issues/247
class Api(BaseApi):
    def _register_doc(self, app_or_blueprint):
        # HINT: This is just a copy of the original implementation with the last line commented out.
        if self._add_specs and self._doc:
            # Register documentation before root if enabled
            app_or_blueprint.add_url_rule(self._doc, 'doc', self.render_doc)
        #app_or_blueprint.add_url_rule(self._doc, 'root', self.render_root)
    @property
    def base_path(self):
        return ''

######################################################################
# Configure Swagger before initilaizing it
######################################################################
api = Api(app,
          version='1.0.0',
          title='Customer REST API Service of the NYU DevOps team alpha',
          description='This is a customer store server.',
          doc='/doc'
         )

# This namespace is the start of the path i.e., /cutomers
ns = api.namespace('customers', description='Customer operations')

# Define the model so that the docs reflect what can be sent
Customer_model = api.model('Customer', {
    'id': fields.Integer(readOnly=True,
                         description='The unique id assigned internally by service'),
    'firstname': fields.String(required=True,
                          description='The firstname of the Customers'),
    'lastname': fields.String(required=True,
                              description='The lastname of Customer fish'),
    'valid': fields.Boolean(required=True,
                              description='The valid status of the Customer'),
    'credit_level': fields.Integer(required=True,
                              description='The credit level of the Customer valid'    )
})

######################################################################
# Special Error Handlers
######################################################################
@api.errorhandler(DataValidationError)
def request_validation_error(error):
    """ Handles Value Errors from bad data """
    message = error.message or str(error)
    app.logger.info(message)
    return {'status':400, 'error': 'Bad Request', 'message': message}, 400

@api.errorhandler(DatabaseConnectionError)
def database_connection_error(error):
    """ Handles Database Errors from connection attempts """
    message = error.message or str(error)
    app.logger.critical(message)
    return {'status':500, 'error': 'Server Error', 'message': message}, 500

######################################################################
# GET HOME PAGE
######################################################################
@app.route('/', methods=['GET'])
def index():
    """ Return the home page"""
    # router could not find this function
    return app.send_static_file('index.html')

######################################################################
# GET HEALTH CHECK
######################################################################
@app.route('/healthcheck')
def healthcheck():
    """ Let them know our heart is still beating """
    return make_response(jsonify(status=200, message='Healthy'), status.HTTP_200_OK)

######################################################################
# CLEAR THE DATABASE
######################################################################
@app.route('/customers/reset', methods=['DELETE'])
def customers_reset():
    """ Removing all the customers from the database"""
    Customer.remove_all()
    return make_response(jsonify(status=200, message='Customer resetted.'), status.HTTP_200_OK)


######################################################################
#  PATH: /customers/{id}
######################################################################
@ns.route('/<int:customer_id>')
@ns.param('customer_id', 'The customer identifier')
class CustomerResource(Resource):
    """
    CustomerResource class
    Allows the manipulation of a single Customer
    GET /Customer{id} - Returns a Customer with the id
    PUT /Customer{id} - Update a Customer with the id
    DELETE /Customer{id} -  Deletes a Customer with the id
    """
    #------------------------------------------------------------------
    # RETRIEVE A Customer
    #------------------------------------------------------------------
    @ns.doc('get_customers')
    @ns.response(404, 'Customer not found')
    @ns.marshal_with(Customer_model)
    def get(self, customer_id):
        """
        Retrieve a single Customer

        This endpoint will return a Customer based on it's id
        """
        app.logger.info("Request to Retrieve a Customer with id [%s]", customer_id)
        customer = Customer.find(customer_id)
        if not customer:
            raise NotFound("Customer with id '{}' was not found.".format(customer_id))
        return customer.serialize(), status.HTTP_200_OK

    #------------------------------------------------------------------
    # UPDATE AN EXISTING Customer
    #------------------------------------------------------------------
    @ns.doc('update_customer')
    @ns.response(404, 'Customer not found')
    @ns.response(400, 'The posted Customer data was not valid')
    @ns.expect(Customer_model)
    @ns.marshal_with(Customer_model)
    def put(self, customer_id):
        """
        Update a Customer

        This endpoint will update a Customer based the body that is posted
        """
        app.logger.info('Request to Update a customer with id [%s]', customer_id)
        check_content_type('application/json')
        customer = Customer.find(customer_id)
        if not customer:
            raise NotFound("Customer with id '{}' was not found.".format(customer_id))
        data = api.payload
        app.logger.info(data)
        # rewrite this function in the future
        # might be buggy
        customer.deserialize(data)
        customer.id = customer_id
        customer.save()
        return customer.serialize(), status.HTTP_200_OK

    #------------------------------------------------------------------
    # DELETE A Customer
    #------------------------------------------------------------------
    @ns.doc('delete_customers')
    @ns.response(204, 'Customer deleted')
    def delete(self, customer_id):
        """
        Delete a Customer

        This endpoint will delete a Customer based the id specified in the path
        """
        app.logger.info('Request to Delete a Customer with id [%s]', customer_id)
        customer = Customer.find(customer_id)
        if customer:
            customer.delete()
        return '', status.HTTP_204_NO_CONTENT


######################################################################
#  PATH: /customers
######################################################################
@ns.route('/', strict_slashes=False)
class CustomerCollection(Resource):
    """ Handles all interactions with collections of Customers """
    #------------------------------------------------------------------
    # Query Customers
    #------------------------------------------------------------------
    @ns.doc('query_customers')
    @ns.response(404, 'Customer not found')
    @ns.marshal_list_with(Customer_model)
    def get(self):
        """ Returns a Query of the Customers """
        app.logger.info('Request to query Customers...')
        # set_trace()
        search_keywords = request.args.keys()
        for search_keyword in search_keywords:
            if search_keyword != 'lastname' and search_keyword != 'firstname':
                raise BadRequest('Can only use lastname or firstname to search.')
        last_name = request.args.get('lastname')
        first_name = request.args.get('firstname')
        if last_name and first_name:
             customers_match_lastname = Customer.find_by_lastname(last_name)
             customers_match_firstname = Customer.find_by_firstname(first_name)
             customers = list(set(customers_match_lastname) & set(customers_match_firstname))
        elif last_name:
            customers = Customer.find_by_lastname(last_name)
        elif first_name:
            customers = Customer.find_by_firstname(first_name)
        else:
            customers = Customer.all()
        # set_trace()
        if not customers:
            raise NotFound("No Customers")
        results = [customer.serialize() for customer in customers]
        app.logger.info('[%s] Customer returned', len(results))
        return results, status.HTTP_200_OK

    #------------------------------------------------------------------
    # ADD A NEW Customer
    #------------------------------------------------------------------
    @ns.doc('create_customers')
    @ns.expect(Customer_model)
    @ns.response(400, 'The posted data was not valid')
    @ns.response(201, 'Customer created successfully')
    @ns.marshal_with(Customer_model, code=201)
    def post(self):
        """
        Creates a Customer
        This endpoint will create a Customer based the data in the body that is posted
        """
        app.logger.info('Request to Create a customer')
        check_content_type('application/json')
        customer = Customer()
        app.logger.info('Payload = %s', api.payload)
        customer.deserialize(api.payload)
        customer.save()
        app.logger.info('Customer with new id [%s] saved!', customer.id)
        location_url = api.url_for(CustomerResource, customer_id=customer.id, _external=True)
        return customer.serialize(), status.HTTP_201_CREATED, {'Location': location_url}


######################################################################
#  PATH: /customers/{id}/upgrade-credit
######################################################################
@ns.route('/<int:customer_id>/upgrade-credit')
@ns.param('customer_id', 'The Customer identifier')
class UpgradeCreditResource(Resource):
    """ Upgrade Credit Action on Customer """
    @ns.doc('upgrade-credit')
    @ns.response(404, 'Customer not found')
    def put(self, customer_id):
        """
        Upgrade credit level of a customers

        This endpoint will increment the credit level of a customer.
        And if credit level becomes positive the valid status of the customer will be True.
        """
        app.logger.info('Request to upgrade credit_level of a customer')
        customer = Customer.find(customer_id)
        if not customer:
            abort(status.HTTP_404_NOT_FOUND, 'Customer with id [{}] was not found.'.format(customer_id))
        customer.upgrade_credit_level()
        customer.save()
        app.logger.info('Credit level of customer with id [%s] has been upgraded!', customer.id)
        return customer.serialize(), status.HTTP_200_OK


######################################################################
#  PATH: /customers/{id}/downgrade-credit
######################################################################
@ns.route('/<int:customer_id>/downgrade-credit')
@ns.param('customer_id', 'The Customer identifier')
class DowngradeCreditResource(Resource):
    """ Downgrade Credit Action on Customer  """
    @ns.doc('downgrade-credit')
    @ns.response(404, 'Customer not found')
    def put(self, customer_id):
        """
        Downgrade credit level of a customers

        This endpoint will decrease the credit level of a customer.
        And if credit level becomes negative the valid status of the customer will be False.
        """
        app.logger.info('Request to uowngrade credit_level of a customer')
        customer = Customer.find(customer_id)
        if not customer:
            abort(status.HTTP_404_NOT_FOUND, 'Customer with id [{}] was not found.'.format(customer_id))
        customer.downgrade_credit_level()
        customer.save()
        app.logger.info('Credit level of customer with id [%s] has been downgraded!', customer.id)
        return customer.serialize(), status.HTTP_200_OK


######################################################################
#  U T I L I T Y   F U N C T I O N S
######################################################################

@app.before_first_request
def init_db():
    """ Initialies the SQLAlchemy app """
    Customer.init_db()

def data_reset():
    """ Removes all Customers from the database """
    Customers.remove_all()

def check_content_type(content_type):
    """ Checks that the media type is correct """
    if request.headers['Content-Type'] == content_type:
        return
    app.logger.error('Invalid Content-Type: %s', request.headers['Content-Type'])
    abort(status.HTTP_415_UNSUPPORTED_MEDIA_TYPE, 'Content-Type must be {}'.format(content_type))

#@app.before_first_request
def initialize_logging(log_level=logging.INFO):
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
