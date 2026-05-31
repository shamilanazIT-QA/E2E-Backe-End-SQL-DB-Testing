Feature: Database Integrity and Business Logic Testing

  Scenario: Verify the employees table is populated
    Given the database connection is active
    When we query the total number of records in "employees"
    Then the total row count should be greater than 0

  Scenario: Verify the trg_calc_discount trigger calculates correct values
    Given the database connection is active
    When a new dummy sale is inserted into the discounts
    Then the "discounts" table should automatically calculate the expected markdown value