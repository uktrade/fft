Feature: Paste sheet data

  Scenario: Pasting valid sheet data into the edit forecast table
    Given the user selects all rows in the edit forecast table
     When the user pastes valid data
     Then the clipboard data is displayed in the forecast table
