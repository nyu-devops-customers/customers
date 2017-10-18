# Test cases can be run with:
# nosetests
# coverage report -m

""" Test cases for the Customer Service """

import logging
import unittest
import json
from mock import MagicMock, patch
from flask_api import status    # HTTP Status Codes
import server

######################################################################
#  T E S T   C A S E S
######################################################################
class TestCustomerServer(unittest.TestCase):
    """ Customer Server Tests """

    @classmethod
    def setUpClass(cls):
        """ Run once before all tests """
        server.app.debug = False
        server.initialize_logging(logging.ERROR)

    def setUp(self):
        """ Runs before each test """
        server.Customer.remove_all()
        server.Customer(0, 'fido', 'dog').save()
        server.Customer(0, 'kitty', 'cat').save()
        self.app = server.app.test_client()

    def tearDown(self):
        """ Runs after each test """
        server.Customer.remove_all()

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
        """ Query Customers by Lastname """
        query_info= {'lastname': 'dog'}
        resp = self.app.get('/customers/query', data = json.dumps(query_info), content_type='application/json')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertTrue(len(resp.data) > 0)
        self.assertTrue('fido' in resp.data)
        self.assertFalse('Dada' in resp.data)
        data = json.loads(resp.data)
        query_item = data[0]
        self.assertEqual(query_item['lastname'], 'dog')

    def test_query_customer_list_by_firstname(self):
        """ Query Customers by Name """
        query_info = {'firstname': 'fido'}
        resp = self.app.get('/customers/query', data = json.dumps(query_info), content_type='application/json')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertTrue(len(resp.data) > 0)
        self.assertTrue('fido' in resp.data)
        self.assertFalse('Miamia' in resp.data)
        data = json.loads(resp.data)
        query_item = data[0]
        self.assertEqual(query_item['firstname'], 'fido')

    def test_method_not_allowed(self):
         """ Call a Method thats not Allowed """
         resp = self.app.post('/customers/0')
         self.assertEqual(resp.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    # @patch('server.Customer.find_by_firstname')
    def test_bad_request(self):
        """ Test a Bad Request error from Find By firstname """
        # bad_request_mock.side_effect = ValueError()
        resp = self.app.post('customers', content_type='application/json')
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

    @patch('server.Customer.find_by_firstname')
    def test_mock_search_data(self, customer_find_mock):
        """ Mocking the  """
        customer_find_mock.side_effect = ValueError()
        resp = self.app.get('/customers/query', content_type='application/json')
        self.assertEqual(resp.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)

    def test_415_unsupported_media_type(self):
        """ Update a Customer """
        new_kitty = {'firstname': 'kitty', 'lastname': 'tabby'}
        data = json.dumps(new_kitty)
        resp = self.app.put('/customers/2', data= data, content_type='string')
        self.assertEqual(resp.status_code, status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)


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
