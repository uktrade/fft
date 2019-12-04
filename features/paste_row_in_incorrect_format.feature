Feature: Paste row data in incorrect format

  Scenario: Pasting invalid row data into the edit forecast table
    Given the user selects a row in the edit forecast table
     When the user pastes invalid data
     Then the incorrect format error is displayed
