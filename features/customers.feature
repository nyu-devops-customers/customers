Feature: The customers service back-end
    As a the product owner of the website
    I need a RESTful catalog service
    So that I can keep track of all my customers

Background:
    Given the following customers
        | id | firstname  | lastname | valid   | credit_level  |
        |  1 | Da         | Huo      | True    | 10            |
        |  2 | Huri       | Ma       | True    | 10            |
        |  3 | Yuqian     | Zhang    | True    | 1            |

Scenario: The server is running
    When I visit the "home page"
    Then I should see "Customers RESTful Service" in the title
    And I should not see "404 Not Found"

"""
SEARCH
"""
Scenario: List All Customers
    When I visit the "home page"
    And I press the "search-btn" button
    Then I should see the message "Success" in status bar
    And I should see "Da" in position 1,2 of the "search_results" table
    And I should see "Huo" in position 1,3 of the "search_results" table
    And I should see "Huri" in position 2,2 of the "search_results" table
    And I should see "Ma" in position 2,3 of the "search_results" table
    And I should see "Yuqian" in position 3,2 of the "search_results" table
    And I should see "Zhang" in position 3,3 of the "search_results" table

Scenario: Find by first name
    When I visit the "home page"
    And I set the "first_name_to_search" to "Da"
    And I press the "search-btn" button   
    Then I should see the message "Success" in status bar 
    And I should see "Da" in position 1,2 of the "search_results" table
    And I should see "Huo" in position 1,3 of the "search_results" table


Scenario: Find by last name
    When I visit the "home page"
    And I set the "last_name_to_search" to "Huo"
    And I press the "search-btn" button   
    Then I should see the message "Success" in status bar 
    And I should see "Da" in position 1,2 of the "search_results" table
    And I should see "Huo" in position 1,3 of the "search_results" table


Scenario: Find by Both(first name and last name)
    When I visit the "home page"
    And I set the "first_name_to_search" to "Da"
    And I set the "last_name_to_search" to "Huo"
    And I press the "search-btn" button   
    Then I should see the message "Success" in status bar 
    And I should see "Da" in position 1,2 of the "search_results" table
    And I should see "Huo" in position 1,3 of the "search_results" table

Scenario: Search a not existing Customer
    When I visit the "home page"
    And I set the "first_name_to_search" to "Messi"
    And I press the "search-btn" button
    Then I should see the message "No Customers." in status bar

"""
CREATE
"""
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

"""
RETRIEVE
"""
Scenario: Retrieve an existing Customer
    When I visit the "home page"
    And I set the "id_to_retrive" to "1"
    And I press the "retrieve-btn" button
    Then I should see "Da" in position 1,2 of the "retrieve_results" table
    And I should see "Huo" in position 1,3 of the "retrieve_results" table

Scenario: Retrieve a not existing Customer
    When I visit the "home page"
    And I set the "id_to_retrive" to "5"
    And I press the "retrieve-btn" button
    Then I should see the message "Customer with id '5' was not found." in status bar 

"""
DELETE
"""
Scenario: Delete an existing Customer and Retrieve that Customer
    When I visit the "home page"
    And I set the "id_to_delete" to "2"
    And I press the "delete-btn" button
    When I visit the "home page"
    And I set the "id_to_retrive" to "2"
    When I press the "retrieve-btn" button
    Then I should see the message "Customer with id '2' was not found." in status bar 


Scenario: Delete an existing Customer and Search all Customers
    When I visit the "home page"
    And I set the "id_to_delete" to "3"
    And I press the "delete-btn" button
    And I press the "search-btn" button
    Then I should see the message "Success" in status bar
    And I should see "Da" in position 1,2 of the "search_results" table
    And I should see "Huo" in position 1,3 of the "search_results" table
    And I should see "Huri" in position 2,2 of the "search_results" table
    And I should see "Ma" in position 2,3 of the "search_results" table
    When I visit the "home page"
    And I set the "id_to_retrive" to "3"
    When I press the "retrieve-btn" button
    Then I should see the message "Customer with id '3' was not found." in status bar

"""
UPDATE
"""
Scenario: Update an existing Customer
    When I visit the "home page"
    When I set the "id_to_update" to "1"
    And I set the "first_name_to_update" to "Danial"
    And I set the "last_name_to_update" to "Huo"
    And I press the "update-btn" button
    Then I should see the message "Success" in status bar
    And I should see "Danial" in position 1,2 of the "update_results" table
    When I visit the "home page"
    And I press the "search-btn" button
    Then I should see the message "Success" in status bar
    And I should see "Danial" in position 1,2 of the "search_results" table
    And I should see "Huo" in position 1,3 of the "search_results" table
    And I should see "Huri" in position 2,2 of the "search_results" table
    And I should see "Ma" in position 2,3 of the "search_results" table
    And I should see "Yuqian" in position 3,2 of the "search_results" table
    And I should see "Zhang" in position 3,3 of the "search_results" table

Scenario: Update a not existing Customer
    When I visit the "home page"
    And I set the "id_to_update" to "4"
    And I set the "first_name_to_update" to "Dada"
    And I set the "last_name_to_update" to "Huo"
    And I press the "update-btn" button
    Then I should see the message "Customer with id '4' was not found." in status bar

Scenario: Update an existing Customer and Retrieve that Customer
    When I visit the "home page"
    When I set the "id_to_update" to "1"
    And I set the "first_name_to_update" to "Dada"
    And I set the "last_name_to_update" to "Huo"
    And I press the "update-btn" button
    Then I should see the message "Success" in status bar
    And I should see "Dada" in position 1,2 of the "update_results" table
    And I should see "Huo" in position 1,3 of the "update_results" table
    When I visit the "home page"
    When I set the "id_to_retrive" to "1"
    And I press the "retrieve-btn" button
    Then I should see "Dada" in position 1,2 of the "retrieve_results" table
    And I should see "Huo" in position 1,3 of the "retrieve_results" table
"""
ACTION: UPGRADE/DOWNGTADE
"""

Scenario: Updgrade Credit Level of a nonexistent Customer
    When I visit the "home page"
    When I set the "id_to_grade" to "5"
    And I press the "upgrade-btn" button
    Then I should see the message "Customer with id [5] was not found." in status bar

Scenario: Upgrade Credit Level of an existing Customer
    When I visit the "home page"
    When I set the "id_to_grade" to "1"
    And I press the "upgrade-btn" button
    Then I should see the message "Success" in status bar
    And I should see "Da" in position 1,2 of the "grade_results" table
    And I should see "Huo" in position 1,3 of the "grade_results" table
    And I should see "11" in position 1,4 of the "grade_results" table
    When I visit the "home page"
    And I press the "search-btn" button
    Then I should see the message "Success" in status bar
    And I should see "Da" in position 1,2 of the "search_results" table
    And I should see "Huo" in position 1,3 of the "search_results" table
    And I should see "11" in position 1,4 of the "search_results" table
    And I should see "Huri" in position 2,2 of the "search_results" table
    And I should see "Ma" in position 2,3 of the "search_results" table
    And I should see "10" in position 2,4 of the "search_results" table
    And I should see "Yuqian" in position 3,2 of the "search_results" table
    And I should see "Zhang" in position 3,3 of the "search_results" table
    And I should see "1" in position 3,4 of the "search_results" table


Scenario: Degrade Credit Level of an existing Customer
    When I visit the "home page"
    When I set the "id_to_grade" to "1"
    And I press the "degrade-btn" button
    Then I should see the message "Success" in status bar
    And I should see "Da" in position 1,2 of the "grade_results" table
    And I should see "Huo" in position 1,3 of the "grade_results" table
    And I should see "9" in position 1,4 of the "grade_results" table


Scenario: Degrade Credit Level below 0 of an existing Customer
    When I visit the "home page"
    When I set the "id_to_grade" to "3"
    And I press the "degrade-btn" button
    And I press the "degrade-btn" button
    Then I should see the message "Success" in status bar
    And I should see "Yuqian" in position 1,2 of the "grade_results" table
    And I should see "Zhang" in position 1,3 of the "grade_results" table
    And I should see "-1" in position 1,4 of the "grade_results" table
    And I should see "false" in position 1,5 of the "grade_results" table
    When I set the "id_to_grade" to "3"
    And I press the "upgrade-btn" button
    Then I should see the message "Success" in status bar
    And I should see "0" in position 1,4 of the "grade_results" table
    And I should see "true" in position 1,5 of the "grade_results" table
