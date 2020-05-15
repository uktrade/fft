Feature: Paste forecast sheet data

  Scenario: Pasting valid sheet data into the edit forecast table
    Given the user selects all rows in the edit forecast table
     When the user pastes valid sheet data
     Then the clipboard data is displayed in the forecast table

  Scenario: Pasting too few rows into sheet
    Given the user selects all rows in the edit forecast table
     When the user pastes valid row data
     Then the too few rows error is displayed

  Scenario: Pasting too many rows into the edit forecast table
    Given the user selects all rows in the edit forecast table
     When the user pastes too many rows
     Then the too many rows error is displayed

  Scenario: Pasting valid data with column headers
     Given the user selects all rows in the edit forecast table
     When the user pastes valid sheet data with column headers
     Then the clipboard data is displayed in the forecast table

  Scenario: Pasting data with invalid column headers
     Given the user selects all rows in the edit forecast table
     When the user pastes sheet data with invalid column headers
     Then the too many rows error is displayed

  Scenario: Pasting valid data with no changes
     Given the user selects all rows in the edit forecast table
     When the user pastes valid sheet with no changes
     Then no message is displayed