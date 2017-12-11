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

## RESTful API

### 1.Return all of the customers with no input 
  
    get /customers/<customer_id>


### 2.Retrieve a single customer with input "customer_id"
   
    get /customers


### 3.Add a new Customer with no input

    post /customers


### 4.Update an exsiting customers with input "customer_id"

    put /customers/<customer_id>


### 5.Increase the credit of a customer with input "customer_id"

    put /customers/<customer_id>/upgrade-credit


### 6.Decrese the credit of a customer with input "customer_id"
    
    put /customers/<customer_id>/degrade-credit


### 7.Delete A customer with input "customer_id"
    
    delete /accounts/<customer_id>


## Running the code

You can run the code to test it out in your browser with the following command:

    $ python run.py
    
You should be able to see it at: http://localhost:5000/

When you are done, you can use `Ctrl+C` to stop the server and then exit and shut down the vm with:

    $ exit
    $ vagrant halt
	 
If the VM is no longer needed you can remove it with:
	
    $ vagrant destroy

## Tests
### Test coverage
You can run the tests using `nosetests`

    $ nosetests

Run Code Coverage to see how well your test cases exercise your code:

    $ coverage run test_server.py
    $ coverage report -m --include=server.py

You can even run `nosetests` with `coverage`

    $ nosetests --with-coverage --cover-package=server

## Behavior Tests
You can run the code to test it out in your browser with the following command:

    $ python run.py
    
You should be able to see it at: http://localhost:5000/
    
Run the tests using behave to see if all scenarios pass

    $ behave

## Swagger

You can then run the server with:
    
    $ python run.py

Finally you can see the microservice Swagger docs at: http://localhost:5000/

	 
## What's featured in the project?

**app/server.py** - the main Service using Python Flask-RESTPlus for Swagger

**models.py** -- hold model definitions of resource

**tests/test_server.py** -- test cases using unittest for the microservice

**tesets/Customer_test.py** -- test cases using unittest for customer model




