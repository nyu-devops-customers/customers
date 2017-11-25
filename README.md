# Customers

[![Build Status](https://travis-ci.org/nyu-devops-customers/customers.svg?branch=master)](https://travis-ci.org/nyu-devops-customers/customers)

This is the working repository of the customer team for NYU DevOps Fall 2017.

## Setup
From a terminal navigate to a location where you want this application code to be downloaded to and issue:
```bash
    $ git clone https://github.com/nyu-devops-customers/customers.git
    $ cd customers
    $ vagrant up
    $ vagrant ssh
    $ cd /vagrant
```
This will place you into an Ubuntu VM all set to run the code.

## Calls

### 1.Return all of the customers with no input 
get `/customers/<customer_id>`

```bash
query_customers():
```

### 2.Retrieve a single customer with input "customer_id"
get `/customers`

```bash
get_customers(customer_id):
```

### 3.Add a new Customer with no input

post `/customers`

```bash
create_customers():
```

### 4.Update an exsiting customers with input "customer_id"

put `/customers/<customer_id>`

```bash
update_customers(customer_id):
```

### 5.Increase the credit of a customer with input "customer_id"

put `/customers/<customer_id>/upgrade-credit`

```bash
upgrade_customers_credit(customer_id):
```

### 6.Decrese the credit of a customer with input "customer_id"
put `/customers/<customer_id>/degrade-credit`

```bash
degrade_customers_credit(customer_id):
```

### 7.Delete A customer with input "customer_id"
delete `/accounts/<customer_id>`

```bash
delete_customers(customer_id):
```
## Tests
### Test coverage
You can run the tests using `nosetests``

    $ nosetests

Run Code Coverage to see how well your test cases exercise your code:

    $ coverage run test_server.py
    $ coverage report -m --include=server.py

You can even run `nosetests` with `coverage`

    $ nosetests --with-coverage --cover-package=server


### Run server
You can run the code to test it out in your browser with the following command:

    $ python server.py

You should be able to see it at: http://localhost:5000/

When you are done, you can use `Ctrl+C` to stop the server and then exit and shut down the vm with:

	 $ exit
	 $ vagrant halt
	 
	 
## What's featured in the project?

**Procfile** - Contains the command to run when you application starts on Bluemix. It is represented in the form `web: <command>` where `<command>` in this sample case is to run the `py` command and passing in the the `server.py` script.

**requirements.txt** - Contains the external python packages that are required by the application. 

**runtime.txt** - Controls which python runtime to use. We use python-2.7.13

**travis.yml** -- the Travis CI file that automates testing

**README.md** - give user instructions how to run and test code.

**manifest.yml** - Controls how the app will be deployed in Bluemix and specifies memory and other services like Redis that are needed to be bound to it.

**server.py** - the main python application. This is implemented as a simple [Flask](http://flask.pocoo.org/) application. The routes are defined in the application using the @app.route() calls. This application has a `/` route and a `/customers` route defined. 

**test_server.py** -- test cases using unittest

**Customer_test.py** -- test cases only for customer model

**models.py** -- hold model definitions of resource

**vcap_services.py** -- Cloud Foundry VCAP_SERVICES support

**db_create.py** -- used to create the database


