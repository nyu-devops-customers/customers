"""
Customer Steps

Steps file for Customer.feature
"""

from os import getenv
import json, time
import requests
from behave import *
from app import server

BASE_URL = getenv('BASE_URL', 'http://localhost:5000/')

@given(u'the following customers')
def step_impl(context):
    """ Delete all customers and load new ones """
    headers = {'Content-Type': 'application/json'}
    context.resp = requests.delete(context.base_url + '/customers/reset', headers=headers)
    assert context.resp.status_code == 204
    create_url = context.base_url + '/customers'
    for row in context.table:
        data = {
            "firstname": row['firstname'],
            "lastname": row['lastname'],
            "valid": row['valid'] in ['True', 'true', '1'],
            "credit_level": row['credit_level']
            }
        payload = json.dumps(data)
        context.resp = requests.post(create_url, data=payload, headers=headers)
        assert context.resp.status_code == 201

@when(u'I visit the "home page"')
def step_impl(context):
    """ Make a call to the base URL """
    context.driver.get(context.base_url)

@then(u'I should see "{message}" in the title')
def step_impl(context, message):
    """ Check the document title for a message """
    assert message in context.driver.title

@then(u'I should not see "{message}"')
def step_impl(context, message):
    assert message not in context.resp.text

@when(u'I set the "{element_id}" to "{text_string}"')
def step_impl(context, element_id, text_string):
    input_box = context.driver.find_element_by_id(element_id)
    input_box.clear()
    input_box.send_keys(text_string)

##################################################################
# This code works because of the following naming convention:
# The buttons have an id in the html hat is the button text
# in lowercase followed by '-btn' so the Clean button has an id of
# id='clear-btn'. That allows us to lowercase the name and add '-btn'
# to get the element id of any button
##################################################################

@when(u'I press the "{btn_id}" button')
def step_impl(context, btn_id):
    btn = context.driver.find_element_by_id(btn_id)
    btn.click()
    time.sleep(2)

@then(u'I should see "{name}" in the results')
def step_impl(context, name):
    element = context.driver.find_element_by_id('search_results')
    print(element.text)
    assert name in element.text

@then(u'I should not see "{name}" in the results')
def step_impl(context, name):
    element = context.driver.find_element_by_id('search_results')
    print(element.text)
    assert name not in element.text

@then(u'I should see the message "{message}"')
def step_impl(context, message):
    element = context.driver.find_element_by_id('flash_message')
    print(element.text)
    assert message in element.text

##################################################################
# This code works because of the following naming convention:
# The id field for text input in the html is the element name
# prefixed by 'pet_' so the Name field has an id='pet_name'
# We can then lowercase the name and prefix with pet_ to get the id
##################################################################

@then(u'I should see "{text_string}" in the "{table_id}" table')
def step_impl(context, text_string, table_id):
    table = context.driver.find_element_by_id(table_id)
    rows = table.find_elements_by_xpath(".//tr")
    for row in rows:
        text = row.text
        print(text)
        if text.find(text_string) > 0:
            return
    assert 0
