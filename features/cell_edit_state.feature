Feature: Paste data to row

  Scenario: Pasting a valid row into the edit forecast table
    Given the user selects a row in the edit forecast table
     When the user pastes valid row data
     Then the clipboard data is displayed in the forecast table
