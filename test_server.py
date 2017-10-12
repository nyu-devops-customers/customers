# Test cases can be run with:
# nosetests
# coverage report -m

""" Test cases for the Customer Service """

import logging
import unittest
import json
#from mock import MagicMock, patch
#from flask_api import status    # HTTP Status Codes
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
#        server.initialize_logging(logging.ERROR)

    def setUp(self):
        """ Runs before each test """
        server.Customer.remove_all()
        server.Customer(0, 'William', 'Smith').save()
        server.customer(0, 'Scott', 'Sun').save()
        self.app = server.app.test_client()

    def tearDown(self):
        """ Runs after each test """
        server.Customer.remove_all()

    def test_index(self):
        """ Test the Home Page """
        resp = self.app.get('/')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = json.loads(resp.data)
        self.assertEqual(data['firstname'], 'Customer Demo REST API Service')

    def test_get_customer_list(self):
        """ Get a list of Customers """
        resp = self.app.get('/customers')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = json.loads(resp.data)
        self.assertEqual(len(data), 2)

    def test_get_customer(self):
        """ Get one customer """
        resp = self.app.get('/customer/2')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = json.loads(resp.data)
        self.assertEqual(data['fistname'], 'Scott')

    def test_get_customer_not_found(self):
        """ Get a Customer thats not found """
        resp = self.app.get('/customers/0')
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_customer(self):
        """ Create a customer """
        # save the current number of customers for later comparrison
        customer_count = self.get_customer_count()
        # add a new customer
        new_customer = {'firstname': 'Yuxi', 'lastname': 'Zhang'}
        data = json.dumps(new_customer)
        resp = self.app.post('/customers', data=data, content_type='application/json')
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        # Make sure location header is set
        location = resp.headers.get('Location', None)
        self.assertIsNotNone(location)
        # Check the data is correct
        new_json = json.loads(resp.data)
        self.assertEqual(new_json['firstname'], 'Yuxi')
        # check that count has gone up and includes sammy
        resp = self.app.get('/customers')
        data = json.loads(resp.data)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(len(data), customert_count + 1)
        self.assertIn(new_json, data)

    def test_update_customer(self):
        """ Update a customer """
        new_customer_scott = {'fistname': 'scott', 'lastname': 'sun'}
        data = json.dumps(new_customer_scott)
        resp = self.app.put('/customers/2', data=data, content_type='application/json')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        resp = self.app.get('/customers/2', content_type='application/json')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        new_json = json.loads(resp.data)
        self.assertEqual(new_json['lastname'], 'sun')

    def test_update_customer_with_no_name(self):
        """ Update a Customer with no name """
        new_customer = {'lastname': 'chen'}
        data = json.dumps(new_customer)
        resp = self.app.put('/customers/2', data=data, content_type='application/json')
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_customer_not_found(self):
        """ Update a Customer that can't be found """
        new_customer = {"lastname": "huri", "firstname": "horse"}
        data = json.dumps(new_customer)
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
        new_customer = {'lastname': 'Dog'}
        data = json.dumps(new_customer)
        resp = self.app.post('/customers', data=data, content_type='application/json')
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_nonexisting_customer(self):
        """ Get a Customer that doesn't exist """
        resp = self.app.get('/customers/5')
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)

    def test_query_customer_list_by_lastname(self):
        """ Query Customers by Category """
        resp = self.app.get('/customers', query_string='lastname = sun')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertTrue(len(resp.data) > 0)
        self.assertTrue('scott' in resp.data)
        self.assertFalse('kitty' in resp.data)
        data = json.loads(resp.data)
        query_item = data[0]
        self.assertEqual(query_item['lastname'], 'sun')

    def test_query_customer_list_by_name(self):
        """ Query Customers by Name """
        resp = self.app.get('/customers', query_string='firstname=Yuxi')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertTrue(len(resp.data) > 0)
        self.assertTrue('Yuxi' in resp.data)
        self.assertFalse('kitty' in resp.data)
        data = json.loads(resp.data)
        query_item = data[0]
        self.assertEqual(query_item['firstname'], 'Yuxi')

    # def test_method_not_allowed(self):
    #     """ Call a Method thats not Allowed """
    #     resp = self.app.post('/customers/0')
    #     self.assertEqual(resp.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    # @patch('server.customer.find_by_name')
    # def test_bad_request(self, bad_request_mock):
    #     """ Test a Bad Request error from Find By Name """
    #     bad_request_mock.side_effect = ValueError()
    #     resp = self.app.get('/customers', query_string='name=fido')
    #     self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

    # @patch('server.customer.find_by_name')
    # def test_mock_search_data(self, customer_find_mock):
    #     """ Test showing how to mock data """
    #     customer_find_mock.return_value = [MagicMock(serialize=lambda: {'name': 'fido'})]
    #     resp = self.app.get('/customers', query_string='name=fido')
    #     self.assertEqual(resp.status_code, status.HTTP_200_OK)


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
