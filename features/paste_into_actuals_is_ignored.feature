Feature: Paste into actuals is ignored

  Scenario: Pasting valid sheet data into the edit forecast table with actuals changed
    Given the user selects a row in the edit forecast table
     When the user pastes valid data with actuals changed
     Then the actuals data is unchanged
