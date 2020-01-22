Feature: Totals update when editing cell

  Scenario: User changes cell value and totals update
    Given the user edits a cell value
     When the user tabs to a new cell
     Then the totals are updated
