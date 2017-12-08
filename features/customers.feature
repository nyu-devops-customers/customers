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

Scenario: Create a Customer
    When I visit the "home page"
    And I set the "first_name_to_create" to "Biqi"
    And I set the "last_name_to_create" to "Lin"
    And I press the "create-btn" button
    Then I should see the message "Success"

Scenario: List All Customers
    When I visit the "home page"
    And I press the "search-btn" button
    Then I should see "Da Huo" in the "search_results" table
    And I should see "Huri Ma" in the "search_results" table
    And I should see "Yuqian Zhang" in the "search_results" table

Scenario: Update a Customer
    When I visit the "home page"
    And I set the "id_to_retrive" to "1"
    And I press the "retrieve-btn" button
    Then I should see "Da Huo" in the "retrieve_results" table
    When I set the "first_name_to_update" to "Danial"
    And I set the "last_name_to_update" to "Huo"
    And I set the "id_to_update" to "1"
    And I press the "update-btn" button
    Then I should see the message "Success"
    When I set the "id_to_retrive" to "1"
    And I press the "retrieve-btn" button
    Then I should see "Danial Huo" in the "retrieve_results" table
