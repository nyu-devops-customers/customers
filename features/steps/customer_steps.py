"""
Customer Steps

Steps file for Customer.feature
"""

from os import getenv
import json, time
import requests
from behave import *

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions

from compare import expect, ensure
from app import server

WAIT_SECONDS = 30
BASE_URL = getenv('BASE_URL', 'http://localhost:5000/')

@given(u'the following customers')
def step_impl(context):
    """ Delete all customers and load new ones """
    headers = {'Content-Type': 'application/json'}
    context.resp = requests.delete(context.base_url + '/customers/reset', headers=headers)
    # assert context.resp.status_code == 204
    expect(context.resp.status_code).to_equal(204)
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
        # assert context.resp.status_code == 201
        expect(context.resp.status_code).to_equal(201)

@when(u'I visit the "home page"')
def step_impl(context):
    """ Make a call to the base URL """
    context.driver.get(context.base_url)

@then(u'I should see "{message}" in the title')
def step_impl(context, message):
    """ Check the document title for a message """
    # assert message in context.driver.title
    expect(context.driver.title).to_contain(message)


@then(u'I should not see "{message}"')
def step_impl(context, message):
    # assert message not in context.resp.text
    ensure(message not in context.resp.text, True)

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


@then(u'I should see the message "{message}" in status bar')
def step_impl(context, message):
    element = context.driver.find_element_by_id('flash_message')
    print(element.text)
    # assert message in element.text
    expect(element.text).to_contain(message)

##################################################################
# This code works because of the following naming convention:
# The id field for text input in the html is the element name
# prefixed by 'pet_' so the Name field has an id='pet_name'
# We can then lowercase the name and prefix with pet_ to get the id
##################################################################

@then(u'I should see "{text_string}" in all rows of the "{table_id}" table')
def step_impl(context, text_string, table_id):
    # table = context.driver.find_element_by_id(table_id)
    # parsed_table = map(lambda x:x.split(" "), table.text.split("\n"))
    # for row in parsed_table[1:]:
    #     # assert text_string in row
    #     expect(row).to_contain(text_string)
    found = WebDriverWait(context.driver, WAIT_SECONDS).until(
        expected_conditions.text_to_be_present_in_element(
            (By.ID, table_id),
            text_string
        )
    )
    expect(found).to_be(True)

@then(u'I should see "{text_string}" in least one row of the "{table_id}" table')
def step_impl(context, text_string, table_id):
    # table = context.driver.find_element_by_id(table_id)
    # parsed_table = map(lambda x:x.split(" "), table.text.split("\n"))
    # for row in parsed_table:
    #     if text_string in row:
    #         return
    # # assert 0
    # expect (0)
    found = WebDriverWait(context.driver, WAIT_SECONDS).until(
        expected_conditions.text_to_be_present_in_element(
            (By.ID, table_id),
            text_string
        )
    )
    expect(found).to_be(True)

@then(u'I should see "{text_string}" in position {row},{col} of the "{table_id}" table')
def step_impl(context, text_string, row, col, table_id):
    row = int(row)
    col = int(col)
    table = context.driver.find_element_by_id(table_id)
    parsed_table = map(lambda x:x.split(" "), table.text.split("\n"))
    # import ipdb
    # ipdb.set_trace()
    # assert parsed_table[row][col-1] == text_string
    expect(parsed_table[row][col-1]).to_equal(text_string)
#     found = WebDriverWait(context.driver, WAIT_SECONDS).until(
#         expected_conditions.text_to_be_present_in_element(
#             (By.ID, table_id),
#             text_string
#         )
#     )
#     expect(found).to_be(True)

@then(u'I should not see "{text_string}" in position {row},{col} of the "{table_id}" table')
def step_impl(context, text_string, row, col, table_id):
    row = int(row)
    col = int(col)
    table = context.driver.find_element_by_id(table_id)
    parsed_table = map(lambda x:x.split(" "), table.text.split("\n"))
    # import ipdb
    # ipdb.set_trace()
    # assert parsed_table[row][col-1].find(text_string) == -1
    expect(parsed_table[row][col-1]).to_equal(text_string)
