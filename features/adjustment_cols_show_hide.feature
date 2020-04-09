Feature: Adjustment columns are shown/hidden

  Scenario: Adjustment columns are shown
    Given adjustment 1 is set to display
     When the user views the edit forecast page
     Then the adjustment 1 column is shown

  Scenario: Adjustment columns are hidden
    Given adjustment 1 is set to hide
     When the user views the edit forecast page
     Then the adjustment 1 column is hidden
