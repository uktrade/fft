Feature: Edit cell value

  Scenario: Double click puts cell into editing mode
    Given the user wants to edit a cell value
     When the user double clicks an editable cell in the edit forecast table
     Then the cell becomes editable

  Scenario: Tabbing puts cell into editing mode
    Given the user wants to edit a cell value
     When the user tabs to a cell
     Then the cell becomes editable

  Scenario: Tabbing to new cell after making edit saves value
    Given the user edits a cell value
     When the user tabs to a new cell
     Then the value is changed and has the correct format

  Scenario: Shift tabbing from editing cell, makes previous cell editable
    Given the user edits a cell value
     When the user shift tabs to the previous cell
     Then the previous cell is in edit mode
