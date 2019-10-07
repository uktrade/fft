Feature: Paste to multiple cells

  Scenario: When pasting into the edit forecast table, data should be changed to that of the clipboard
    Given the user pastes into the edit forecast table
     When the user checks the forecast table
     Then the clipboard data is displayed
