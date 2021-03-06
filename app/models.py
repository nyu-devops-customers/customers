# Copyright NYU-DevOps-Alpha team-customer. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the 'License');
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an 'AS IS' BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""
Models for Customer Demo Service

All of the models are stored in this module

Models
------
Customer - A Customer used in the Store

Attributes:
-----------
id : int
firstname : string
lastname: string
valid: boolean
credit_level: int

"""

"""
This model uses SQLAlchemy to persist itself
"""

import os
import json
import logging
from . import db
from . import app
from sqlalchemy.exc import DisconnectionError
import pymysql
class DataValidationError(Exception):
    """ Used for an data validation errors when deserializing """
    pass
class DatabaseConnectionError(DisconnectionError):
    """ Used for database connection failure """
    pass


######################################################################
# Customer Model for database
######################################################################
class Customer(db.Model):
    """A single customer"""
    logger = logging.getLogger(__name__)

    # Table Schema
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(63))
    lastname = db.Column(db.String(63))
    valid = db.Column(db.Boolean(), default=True)
    credit_level = db.Column(db.Integer, default=0)

    def upgrade_credit_level(self):
        """ Upgrade the credit level of the customer """
        self.credit_level += 1
        if self.credit_level >= 0:
            self.valid = True

    def downgrade_credit_level(self):
        """ Downgrade the credit level of the customer """
        self.credit_level -= 1
        if self.credit_level < 0:
            self.valid = False

    def save(self):
        """ Saves an existing Customer in the database """
        # if the id is None it hasn't been added to the database
        if not self.id:
            db.session.add(self)
        db.session.commit()

    def delete(self):
        """ Deletes a Customer from the database """
        db.session.delete(self)
        db.session.commit()

    def serialize(self):
        """ Serializes a Customer into a dictionary """
        return {"id": self.id,
                "firstname": self.firstname,
                "lastname": self.lastname,
                "valid": self.valid,
                "credit_level": self.credit_level}

    def deserialize(self, data):
        """ deserializes a Customer my marshalling the data """
        try:
            self.firstname = data['firstname']
            self.lastname = data['lastname']
            if(data.has_key('valid') and data.has_key('credit_level')):
                self.valid= data['valid']
                self.credit_level = data['credit_level']
                if self.credit_level < 0 and self.valid == True:
                    raise DataValidationError('Invalid Customer: Customer with negative credit should not be valid')
                if self.credit_level >= 0 and self.valid == False:
                    raise DataValidationError('Invalid Customer: Customer with non-negative credit should be valid')
        except KeyError as error:
            raise DataValidationError('Invalid Customer: missing ' + error.args[0])
        except TypeError as error:
            raise DataValidationError('Invalid customer: body of request contained' \
                                      'bad or no data')
        return self


######################################################################
#  S T A T I C   D A T A B S E   M E T H O D S
######################################################################
    @staticmethod
    def init_db(reset = False):
        """ Initializes the database session """
        Customer.logger.info('Initializing database')
        # import pdb; pdb.set_trace()
        uri = app.config['SQLALCHEMY_DATABASE_URI']
        Customer.logger.info('Database URI {}'.format(uri))
        try:
            Customer.logger.info("Creating database tables")
            if reset:
                Customer.logger.info('Dropping old tables')
                db.drop_all()
            db.create_all()
        except Exception as error:
            Customer.logger.error('Oops, got error {}'.format(error.message))
            # Parse the URI for user, password, host
            dbname = app.config['DB_NAME']
            host = app.config['DB_HOSTNAME']
            user = app.config['DB_USERNAME']
            password = app.config['DB_PASSWORD']
            # raise DatabaseConnectionError('Could not connect to the clients MySQL Service')
            # Connect and create the database
            try:
                conn = pymysql.connect(host=host, user=user, password=password)
                conn.cursor().execute('create database IF NOT EXISTS {}'.format(dbname))
                Customer.logger.info("Creating database tables")
                db.create_all()
            except Exception as error:
                Customer.logger.error('reconnect database fail! got error {}'.format(error.message))
                raise DatabaseConnectionError('Could not connect to the clients MySQL Service')

    @staticmethod
    def all():
        """ Query that returns all Customers """
        Customer.logger.info('Processing all Customers')
        return Customer.query.all()

    @staticmethod
    def remove_all():
        """ Removes all Customers from the database """
        Customer.logger.info('Removing all Customers')
        Customer.query.delete()
        db.session.commit()

######################################################################
#  F I N D E R   M E T H O D S
######################################################################
    @staticmethod
    def find(customer_id):
        """ Query that finds Customers by their id """
        Customer.logger.info('Processing lookup for id %s ...', customer_id)
        return Customer.query.get(customer_id)

    @staticmethod
    def find_by_kargs(args):
        """ Query that finds Customers by their lastname """
        Customer.logger.info('Processing name query for %s ...', str(args))
        if len(args) == 0:
            return Customer.all()
        q = Customer.query
        try:
            for attr, value in args.items():
                q = q.filter(getattr(Customer, attr) == value)
            return q.all()
        except AttributeError as error:
            raise DataValidationError('Invalid Query String:' + str(args))
