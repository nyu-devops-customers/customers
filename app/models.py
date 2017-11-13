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

"""
import threading

class DataValidationError(Exception):
    """ Used for an data validation errors when deserializing """
    pass

class Customer(object):
    """
    Class that represents a Customer

    This version uses an in-memory collection of Customers for testing
    """
    lock = threading.Lock()
    data = []
    index = 0

    def __init__(self, id=0, firstname='', lastname=''):
        """ Initialize a Customer """
        self.id = id
        self.firstname = firstname
        self.lastname = lastname

    def save(self):
        """
        Saves a Customer to the data store
        """
        if self.id == 0:
            self.id = self.__next_index()
            Customer.data.append(self)
        else:
            for i in range(len(Customer.data)):
                if Customer.data[i].id == self.id:
                    Customer.data[i] = self
                    break

    def delete(self):
        """ Removes a Customer from the data store """
        Customer.data.remove(self)

    def serialize(self):
        """ Serializes a Customer into a dictionary """
        return {"id": self.id, "firstname": self.firstname, "lastname": self.lastname}

    def deserialize(self, data):
        """
        Deserializes a Customer from a dictionary

        Args:
            data (dict): A dictionary containing the Customer data
        """
        if not isinstance(data, dict):
            raise DataValidationError('Invalid Customer: body of request contained bad or no data')
        if data.has_key('id'):
            self.id = data['id']
        try:
            self.firstname = data['firstname']
            self.lastname = data['lastname']
        except KeyError as err:
            raise DataValidationError('Invalid Customer: missing ' + err.args[0])
        return

    @staticmethod
    def __next_index():
        """ Generates the next index in a continual sequence """
        with Customer.lock:
            Customer.index += 1
        return Customer.index

    @staticmethod
    def all():
        """ Returns all of the Customers in the database """
        return [customer for customer in Customer.data]

    @staticmethod
    def remove_all():
        """ Removes all of the Customers from the database """
        del Customer.data[:]
        Customer.index = 0
        return Customer.data

    @staticmethod
    def find(customer_id):
        """ Finds a Customer by it's ID """
        if not Customer.data:
            return None
        customers = [customer for customer in Customer.data if customer.id == customer_id]
        if customers:
            return customers[0]
        return None

    @staticmethod
    def find_by_lastname(lastname):
        """ Returns all of the Customers in a lastname

        Args:
            lastname (string): the lastname of the Customers you want to match
        """
        return [customer for customer in Customer.data if customer.lastname == lastname]

    @staticmethod
    def find_by_firstname(firstname):
        """ Returns all Customers with the given firstname

        Args:
            firstname (string): the firstname of the Customers you want to match
        """
        return [customer for customer in Customer.data if customer.firstname == firstname]
