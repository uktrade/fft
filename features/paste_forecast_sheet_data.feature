Feature: Paste forecast sheet data

  Scenario: Pasting valid sheet data into the edit forecast table
    Given the user selects all rows in the edit forecast table
     When the user pastes valid sheet data
     Then the clipboard data is displayed in the forecast table

  Scenario: Pasting too few rows into sheet
    Given the user selects all rows in the edit forecast table
     When the user pastes valid row data
     Then the too few rows error is displayed

  Scenario: Pasting a valid row into the edit forecast table
    Given the user selects all rows in the edit forecast table
     When the user pastes too many rows
     Then the too many rows error is displayed
