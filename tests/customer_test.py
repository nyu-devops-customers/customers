# Test cases can be run with:
# nosetests
# coverage report -m

""" Test cases for Customer Model """

import unittest

from app.models import Customer
from app.models import DataValidationError

######################################################################
#  T E S T   C A S E S
######################################################################
class TestCustomers(unittest.TestCase):
    """ Test Cases for Customers """

    def setUp(self):
        Customer.remove_all()

    def test_create_a_Customer(self):
        """ Create a Customer and assert that it exists """
        customer = Customer(0, "fido", "dog")
        self.assertTrue(customer != None)
        self.assertEqual(customer.id, 0)
        self.assertEqual(customer.firstname, "fido")
        self.assertEqual(customer.lastname, "dog")

    def test_add_a_Customer(self):
        """ Create a Customer and add it to the database """
        customer = Customer.all()
        self.assertEqual(customer, [])
        customer = Customer(0, "fido", "dog")
        self.assertTrue(customer != None)
        self.assertEqual(customer.id, 0)
        customer.save()
        # Asert that it was assigned an id and shows up in the database
        self.assertEqual(customer.id, 1)
        customers = Customer.all()
        self.assertEqual(len(customers), 1)

    def test_upgrade_credit_of_a_Customer(self):
        """ Upgrade credit of a Customer """
        customer = Customer(0, "fido", "dog")
        customer.save()
        self.assertEqual(customer.id, 1)
        self.assertEqual(customer.valid, True)
        # Upgrade it and save it
        customer.upgrade_credit_level()
        customer.save()
        self.assertEqual(customer.id, 1)
        self.assertEqual(customer.valid, True)
        self.assertEqual(customer.credit_level, 1)
        customer.upgrade_credit_level()
        customer.save()
        self.assertEqual(customer.credit_level, 2)
        # Fetch it back and make sure the id hasn't changed
        # but the data did change
        customers = Customer.all()
        self.assertEqual(len(customers), 1)
        self.assertEqual(customers[0].valid, True);

    def test_downgrade_credit_of_a_Customer(self):
        """ Downgrade credit of a Customer """
        customer = Customer(0, "fido", "dog")
        customer.save()
        self.assertEqual(customer.id, 1)
        self.assertEqual(customer.valid, True)
        self.assertEqual(customer.credit_level, 0)
        # Downgrade it and save it
        customer.downgrade_credit_level()
        customer.save()
        self.assertEqual(customer.id, 1)
        self.assertEqual(customer.valid, False)
        self.assertEqual(customer.credit_level, -1)
        customer.upgrade_credit_level()
        customer.save()
        self.assertEqual(customer.credit_level, 0)

        # Fetch it back and make sure the id hasn't changed
        # but the data did change
        customers = Customer.all()
        self.assertEqual(len(customers), 1)
        self.assertEqual(customers[0].valid, True);

    def test_update_a_Customer(self):
        """ Update a Customer """
        customer = Customer(0, "fido", "dog")
        customer.save()
        self.assertEqual(customer.id, 1)
        # Change it an save it
        customer.lastname = "k9"
        customer.save()
        self.assertEqual(customer.id, 1)
        # Fetch it back and make sure the id hasn't changed
        # but the data did change
        customers = Customer.all()
        self.assertEqual(len(customers), 1)
        self.assertEqual(customers[0].lastname, "k9")


    def test_delete_a_Customer(self):
        """ Delete a Customer """
        customer = Customer(0, "fido", "dog")
        customer.save()
        self.assertEqual(len(customer.all()), 1)
        # delete the Customer and make sure it isn't in the database
        customer.delete()
        self.assertEqual(len(customer.all()), 0)

    def test_serialize_a_Customer(self):
        """ Test serialization of a Customer """
        customer = Customer(0, "fido", "dog")
        data = customer.serialize()
        self.assertNotEqual(data, None)
        self.assertIn('id', data)
        self.assertEqual(data['id'], 0)
        self.assertIn('firstname', data)
        self.assertEqual(data['firstname'], "fido")
        self.assertIn('lastname', data)
        self.assertEqual(data['lastname'], "dog")
        self.assertEqual(data['valid'], True)
        self.assertEqual(data['credit_level'], 0)


    def test_deserialize_a_Customer(self):
        """ Test deserialization of a Customer """
        data = {"id": 1, "firstname": "kitty", "lastname": "cat", "valid": True, "credit_level": 1}
        customer = Customer()
        customer.deserialize(data)
        self.assertNotEqual(customer, None)
        self.assertEqual(customer.id, 1)
        self.assertEqual(customer.firstname, "kitty")
        self.assertEqual(customer.lastname, "cat")
        self.assertEqual(customer.valid, True)
        self.assertEqual(customer.credit_level, 1)

    def test_deserialize_with_no_name(self):
        """ Deserialize a Customer without a name """
        customer = Customer()
        data = {"id":0, "lastname": "cat"}
        self.assertRaises(DataValidationError, customer.deserialize, data)

    def test_deserialize_with_no_data(self):
        """ Deserialize a Customer with no data """
        customer = Customer()
        self.assertRaises(DataValidationError, customer.deserialize, None)

    def test_deserialize_with_bad_data(self):
        """ Deserailize a Customer with bad data """
        customer = Customer()
        self.assertRaises(DataValidationError, customer.deserialize, "data")

    def test_deserialize_with_invalid_credit_data(self):
        """ Deserailize a Customer with bad data """
        customer = Customer()
        data = {"id": 1, "firstname": "kitty", "lastname": "cat",
            "valid": True, "credit_level": -1}
        self.assertRaises(DataValidationError, customer.deserialize, data)
        data = {"id": 1, "firstname": "kitty", "lastname": "cat",
            "valid": False, "credit_level": 1}
        self.assertRaises(DataValidationError, customer.deserialize, data)

    def test_find_Customer(self):
        """ Find a Customer by ID """
        Customer(0, "fido", "dog").save()
        Customer(0, "kitty", "cat").save()
        customer = Customer.find(2)
        self.assertIsNot(customer, None)
        self.assertEqual(customer.id, 2)
        self.assertEqual(customer.firstname, "kitty")

    def test_find_with_no_Customers(self):
        """ Find a Customer with no Customers """
        customer = Customer.find(1)
        self.assertIs(customer, None)

    def test_Customer_not_found(self):
        """ Test for a Customer that doesn't exist """
        Customer(0, "fido", "dog").save()
        customer = Customer.find(2)
        self.assertIs(customer, None)

    def test_find_by_lastname(self):
        """ Find Customers by Category """
        Customer(0, "fido", "dog").save()
        Customer(0, "kitty", "cat").save()
        customers = Customer.find_by_lastname("cat")
        self.assertNotEqual(len(customers), 0)
        self.assertEqual(customers[0].lastname, "cat")
        self.assertEqual(customers[0].firstname, "kitty")

    def test_find_by_firstname(self):
        """ Find a Customer by Name """
        Customer(0, "fido", "dog").save()
        Customer(0, "kitty", "cat").save()
        customers = Customer.find_by_firstname("kitty")
        self.assertEqual(len(customers), 1)
        self.assertEqual(customers[0].lastname, "cat")
        self.assertEqual(customers[0].firstname, "kitty")


######################################################################
#   M A I N
######################################################################
if __name__ == '__main__':
    unittest.main()
    # suite = unittest.TestLoader().loadTestsFromTestCase(TestCustomers)
    # unittest.TextTestRunner(verbosity=2).run(suite)