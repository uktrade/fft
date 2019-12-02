Feature: Paste data to row

  Scenario: Pasting a row into the edit forecast table
    Given the user selects a row in the edit forecast table
     When the user pastes
     Then the clipboard data is displayed in the forecast table
