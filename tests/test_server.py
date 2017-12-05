# Test cases can be run with:
# nosetests
# coverage report -m

""" Test cases for the Customer Service """
import os
import logging
import unittest
import json
from mock import MagicMock, patch
from flask_api import status    # HTTP Status Codes
from app.models import Customer

from app import server, db
import app.server as server

# from nose.tools import set_trace

DATABASE_URI = os.getenv('DATABASE_URI', None)
######################################################################
#  T E S T   C A S E S
######################################################################
class TestCustomerServer(unittest.TestCase):
    """ Customer Server Tests """

    @classmethod
    def setUpClass(cls):
        """ Run once before all tests """
        server.app.debug = False
        server.initialize_logging(logging.INFO)
        # Set up the test database
        if DATABASE_URI:
            server.app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URI


    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        server.init_db()
        db.drop_all()    # clean up the last tests
        db.create_all()  # create new tables
        server.Customer(firstname = 'fido', lastname = 'dog').save()
        server.Customer(firstname = 'kitty', lastname = 'cat').save()
        self.app = server.app.test_client()

    def tearDown(self):
        """ Runs after each test """
        db.session.remove()
        db.drop_all()

    def test_index(self):
        """ Test the Home Page """
        resp = self.app.get('/')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resp.content_type, 'text/html; charset=utf-8')

    def test_get_customer_list(self):
        """ Get a list of Customers """
        resp = self.app.get('/customers')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = json.loads(resp.data)
        self.assertEqual(len(data), 2)
        Customer.remove_all()
        resp = self.app.get('/customers')
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_customer(self):
        """ Get one Customer """
        resp = self.app.get('/customers/2')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = json.loads(resp.data)
        self.assertEqual(data['firstname'], 'kitty')

    def test_get_customer_not_found(self):
        """ Get a Customer thats not found """
        resp = self.app.get('/customers/0')
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_customer(self):
        """ Create a Customer """
        # save the current number of customers for later comparrison
        customer_count = self.get_customer_count()
        # add a new customer
        new_customer = {'firstname': 'sammy', 'lastname': 'snake'}
        data = json.dumps(new_customer)
        resp = self.app.post('/customers', data=data, content_type='application/json')
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        # Make sure location header is set
        location = resp.headers.get('Location', None)
        self.assertIsNotNone(location)
        # Check the data is correct
        new_json = json.loads(resp.data)
        self.assertEqual(new_json['firstname'], 'sammy')
        # check that count has gone up and includes sammy
        resp = self.app.get('/customers')
        data = json.loads(resp.data)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(len(data), customer_count + 1)
        self.assertIn(new_json, data)

    def test_update_customer(self):
        """ Update a Customer """
        new_kitty = {'firstname': 'kitty', 'lastname': 'tabby'}
        data = json.dumps(new_kitty)
        resp = self.app.put('/customers/2', data=data, content_type='application/json')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        resp = self.app.get('/customers/2', content_type='application/json')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        new_json = json.loads(resp.data)
        self.assertEqual(new_json['lastname'], 'tabby')

    def test_update_customer_with_invalid_credit(self):
        """ Update a Customer with invalid credit """
        new_kitty = {'firstname': 'kitty', 'lastname': 'tabby', 'valid': True,'credit_level': -1}
        data = json.dumps(new_kitty)
        resp = self.app.put('/customers/2', data=data, content_type='application/json')
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)
        another_kitty = {'firstname': 'kitty', 'lastname': 'tabby', 'valid': False,'credit_level': 1}
        data = json.dumps(another_kitty)
        resp = self.app.put('/customers/2', data=data, content_type='application/json')
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_customer_with_no_firstname(self):
        """ Update a Customer with no firstname """
        new_customer = {'lastname': 'dog'}
        data = json.dumps(new_customer)
        resp = self.app.put('/customers/2', data=data, content_type='application/json')
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_customer_not_found(self):
        """ Update a Customer that can't be found """
        new_kitty = {"firstname": "timothy", "lastname": "mouse"}
        data = json.dumps(new_kitty)
        resp = self.app.put('/customers/0', data=data, content_type='application/json')
        self.assertEquals(resp.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_customer(self):
        """ Delete a Customer that exists """
        # save the current number of customers for later comparrison
        customer_count = self.get_customer_count()
        # delete a customer
        resp = self.app.delete('/customers/2', content_type='application/json')
        self.assertEqual(resp.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(len(resp.data), 0)
        new_count = self.get_customer_count()
        self.assertEqual(new_count, customer_count - 1)

    def test_create_customer_with_no_firstname(self):
        """ Create a Customer with the name missing """
        new_customer = {'lastname': 'dog'}
        data = json.dumps(new_customer)
        resp = self.app.post('/customers', data=data, content_type='application/json')
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_nonexisting_customer(self):
        """ Get a Customer that doesn't exist """
        resp = self.app.get('/customers/5')
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)

    def test_query_customer_list_by_lastname(self):
        """ Query Customers by Last Name """
        resp = self.app.get('/customers?lastname=dog', content_type='application/json')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertTrue(len(resp.data) > 0)
        self.assertTrue('fido' in resp.data)
        self.assertFalse('Dada' in resp.data)
        data = json.loads(resp.data)
        query_item = data[0]
        self.assertEqual(query_item['lastname'], 'dog')

    def test_query_customer_list_by_firstname(self):
        """ Query Customers by Fisrt Name """
        resp = self.app.get('/customers?firstname=fido', content_type='application/json')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertTrue(len(resp.data) > 0)
        self.assertTrue('fido' in resp.data)
        self.assertFalse('Miamia' in resp.data)
        data = json.loads(resp.data)
        query_item = data[0]
        self.assertEqual(query_item['firstname'], 'fido')
        server.Customer.remove_all()
        resp = self.app.get('/customers?firstname=fido', content_type='application/json')
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)

    def test_query_customer_list_by_unsupported_field(self):
        """ Query Customers by None Parameter"""
        resp = self.app.get('/customers?gender=male', content_type='application/json')
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

    def test_query_no_customer(self):
        """ Query used when no custome is avaliable """
        server.Customer.remove_all()
        resp = self.app.get('/customers?lastname=dog', content_type='application/json')
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)

    def test_method_not_allowed(self):
         """ Call a Method thats not Allowed """
         resp = self.app.post('/customers/0')
         self.assertEqual(resp.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    @patch('app.server.Customer.find_by_firstname')
    def test_mock_search_data_internal_error(self, customer_find_mock):
        """ Mocking the Server Internal Error """
        customer_find_mock.side_effect = OSError()
        resp = self.app.get('/customers?firstname=fido', content_type='application/json')
        self.assertEqual(resp.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)

    def test_415_unsupported_media_type(self):
        """ Test the media type checking handler """
        new_kitty = {'firstname': 'kitty', 'lastname': 'tabby'}
        data = json.dumps(new_kitty)
        resp = self.app.put('/customers/2', data= data, content_type='string')
        self.assertEqual(resp.status_code, status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)

    def test_upgrade_credit_of_a_Customer(self):
        """ Upgrade the credit of a customer"""
        resp = self.app.put('/customers/2/upgrade-credit', content_type='application/json')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        new_json = json.loads(resp.data)
        self.assertEqual(new_json['credit_level'], 1)
        self.assertEqual(new_json['valid'], True)

    def test_upgrade_credit_of_a_Customer_not_avaliable(self):
        """ Upgrade the credit of a customer not avaliable"""
        resp = self.app.put('/customers/4/upgrade-credit', content_type='application/json')
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)

    def test_downgrade_credit_of_a_Customer(self):
        """ Downgrade the credit of a customer"""
        resp = self.app.put('/customers/2/downgrade-credit', content_type='application/json')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        new_json = json.loads(resp.data)
        self.assertEqual(new_json['credit_level'], -1)
        self.assertEqual(new_json['valid'], False)

    def test_downgrade_credit_of_a_Customer_not_avaliable(self):
        """ Upgrade the credit of a customer not avaliable"""
        resp = self.app.put('/customers/4/downgrade-credit', content_type='application/json')
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)

    def test_the_valid_status_turn_by_credit(self):
        """ Test the turn of valid when changing the credit_level """
        resp = self.app.put('/customers/2/upgrade-credit', content_type='application/json')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        new_json = json.loads(resp.data)
        self.assertEqual(new_json['credit_level'], 1)
        self.assertEqual(new_json['valid'], True)
        resp = self.app.put('/customers/2/downgrade-credit', content_type='application/json')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        new_json = json.loads(resp.data)
        self.assertEqual(new_json['credit_level'], 0)
        self.assertEqual(new_json['valid'], True)
        resp = self.app.put('/customers/2/downgrade-credit', content_type='application/json')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        new_json = json.loads(resp.data)
        self.assertEqual(new_json['credit_level'], -1)
        self.assertEqual(new_json['valid'], False)
        resp = self.app.put('/customers/2/upgrade-credit', content_type='application/json')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        new_json = json.loads(resp.data)
        self.assertEqual(new_json['credit_level'], 0)
        self.assertEqual(new_json['valid'], True)

    def test_health_check(self):
        """ Test the healthcheck url"""
        resp = self.app.get('/healthcheck')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        new_json = json.loads(resp.data)
        self.assertEqual(new_json['message'], 'Healthy')
######################################################################
# Utility functions
######################################################################

    def get_customer_count(self):
        """ save the current number of customers """
        resp = self.app.get('/customers')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = json.loads(resp.data)
        return len(data)


######################################################################
#   M A I N
######################################################################
if __name__ == '__main__':
    unittest.main()
