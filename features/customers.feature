Feature: The customers service back-end
    As a the product owner of the website
    I need a RESTful catalog service
    So that I can keep track of all my customers

Background:
    Given the following customers
        | id | firstname  | lastname | valid   | credit_level  |
        |  1 | Da         | Huo      | True    | 10            |
        |  2 | Huri       | Ma       | True    | 10            |
        |  3 | Yuqian     | Zhang    | True    | 20            |

Scenario: The server is running
    When I visit the "home page"
    Then I should see "Customers RESTful Service" in the title
    And I should not see "404 Not Found"

Scenario: Search All Customers
    When I visit the "home page"
    And I press the "search-btn" button
    Then I should see the message "Success" in status bar
    And I should see "Da" in position 1,2 of the "search_results" table
    And I should see "Huo" in position 1,3 of the "search_results" table
    And I should see "Huri" in position 2,2 of the "search_results" table
    And I should see "Ma" in position 2,3 of the "search_results" table
    And I should see "Yuqian" in position 3,2 of the "search_results" table
    And I should see "Zhang" in position 3,3 of the "search_results" table

Scenario: Create a Customer
    When I visit the "home page"
    And I set the "first_name_to_create" to "Biqi"
    And I set the "last_name_to_create" to "Lin"
    And I press the "create-btn" button
    Then I should see the message "Success" in status bar
    And I should see "Biqi" in position 1,2 of the "create_results" table
    And I should see "Lin" in position 1,3 of the "create_results" table

Scenario: Create and Search all Customers
    When I visit the "home page"
    And I set the "first_name_to_create" to "Biqi"
    And I set the "last_name_to_create" to "Lin"
    And I press the "create-btn" button
    Then I should see the message "Success" in status bar
    And I should see "Biqi" in position 1,2 of the "create_results" table
    And I should see "Lin" in position 1,3 of the "create_results" table
    When I visit the "home page"
    And I press the "search-btn" button
    Then I should see the message "Success" in status bar
    And I should see "Da" in position 1,2 of the "search_results" table
    And I should see "Huo" in position 1,3 of the "search_results" table
    And I should see "Huri" in position 2,2 of the "search_results" table
    And I should see "Ma" in position 2,3 of the "search_results" table
    And I should see "Yuqian" in position 3,2 of the "search_results" table
    And I should see "Zhang" in position 3,3 of the "search_results" table
    And I should see "Biqi" in position 4,2 of the "search_results" table
    And I should see "Lin" in position 4,3 of the "search_results" table

Scenario: Retrieve an existing Customer
    And I set the "id_to_retrive" to "1"
    And I press the "retrieve-btn" button
    Then I should see "Da" in position 1,2 of the "retrieve_reuslts" table
    And I should see "Huo" in position 1,3 of the "retrieve_reuslts" table

Scenario: Retrieve a not existing Customer
    When I visit the "home page"
    And I set the "id_to_retrive" to "5"
    And I press the "retrieve-btn" button
    Then I should see the message "Customer with id '5' was not found. You have requested this URI [/customers/5] but did you mean /customers/ or /customers/reset ?" in status bar

Scenario: Delete an existing Customer
    When I visit the "home page"
    And I set the "id_to_delete" to "3"
    And I press the "delete-btn" button
    Then I should see the message "Success" in status bar

Scenario: Delete a not existing Customer
    When I visit the "home page"
    And I set the "id_to_delete" to "7"
    And I press the "delete-btn" button
    Then I should see the message "Success" in status bar

Scenario: Delete an existing Customer and Retrieve that Customer
    When I visit the "home page"
    And I set the "id_to_delete" to "2"
    And I press the "delete-btn" button
    And I set the "id_to_retrive" to "2"
    When I press the "retrieve-btn" button
    Then I should see the message "Customer with id '2' was not found. You have requested this URI [/customers/2] but did you mean /customers/ or /customers/reset ?" in status bar


Scenario: Delete an existing Customer and Search all Customers
    When I visit the "home page"
    And I set the "id_to_delete" to "2"
    And I press the "delete-btn" button
    When I visit the "home page"
    And I press the "search-btn" button
    Then I should see the message "Success" in status bar
    And I should see "Da" in position 1,2 of the "search_results" table
    And I should see "Huo" in position 1,3 of the "search_results" table
    And I should not see "Huri" in position 2,2 of the "search_results" table
    And I should not see "Ma" in position 2,3 of the "search_results" table
    And I should see "Yuqian" in position 3,2 of the "search_results" table
    And I should see "Zhang" in position 3,3 of the "search_results" table

Scenario: Update an existing Customer
    When I visit the "home page"
    When I set the "id_to_update" to "1"
    And I set the "first_name_to_update" to "Danial"
    And I set the "last_name_to_update" to "Huo"
    And I press the "update-btn" button
    Then I should see the message "Success" in status bar
    And I should see "Danial" in position 1,2 of the "update_results" table
    And I should see "Huo" in position 1,3 of the "update_results" table

Scenario: Update a not existing Customer


Scenario: Update an existing Customer and Retrieve that Customer
    When I visit the "home page"
    When I set the "id_to_update" to "1"
    And I set the "first_name_to_update" to "Danial"
    And I set the "last_name_to_update" to "Huo"
    And I press the "update-btn" button
    Then I should see the message "Success" in status bar
    And I should see "Danial" in position 1,2 of the "update_results" table
    And I should see "Huo" in position 1,3 of the "update_results" table
    When I set the "id_to_retrive" to "1"
    And I press the "retrieve-btn" button
    Then I should see "Danial" in position 1,2 of the "retrieve_results" table
    And I should see "Huo" in position 1,3 of the "retrieve_results" table

Scenario: Update an existing Customer and Search all Customers
