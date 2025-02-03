Feature: Show/hide a forecast column

  Scenario: Clicking the NAC code column hide link hides the NAC code column
    Given the user wants to hide the NAC code column
     When the user clicks the hide NAC code column
     Then the NAC code column is hidden
