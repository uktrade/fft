Feature: Show/hide a forecast column

  Scenario: Clicking the NAC column hide link hides the NAC column
    Given the user wants to hide the NAC column
     When the user clicks the hide NAC column
     Then the NAC column is hidden
