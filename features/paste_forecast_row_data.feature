Feature: Paste forecast row data

  Scenario: Pasting a valid row into the edit forecast table
    Given the user selects a row in the edit forecast table
     When the user pastes valid row data
     Then the clipboard data is displayed in the forecast table

  Scenario: Pasting a valid row with 5 decimals places in amended value
    Given the user selects a row in the edit forecast table
     When the user pastes valid row data with a 5 decimal place value
     Then the clipboard data is displayed in the forecast table

  Scenario: Pasting valid sheet data into the edit forecast table with actuals changed
    Given the user selects a row in the edit forecast table
     When the user pastes valid row data with actuals changed
     Then the actuals data is unchanged

  Scenario: Pasting invalid row data into the edit forecast table
    Given the user selects a row in the edit forecast table
     When the user pastes invalid row data
     Then the incorrect format error is displayed

# Will be reinstated once edit download has adjustment cols
#  Scenario: Pasting too many columns data into the edit forecast table
#    Given the user selects a row in the edit forecast table
#     When the user pastes too many column row data
#     Then the too many columns error message is displayed

  Scenario: Pasting too few columns data into the edit forecast table
    Given the user selects a row in the edit forecast table
     When the user pastes too few column row data
     Then the too few columns error message is displayed

  Scenario: Pasting mismatched columns into the edit forecast table
    Given the user selects a row in the edit forecast table
     When the user pastes mismatched columns
     Then the mismatched columns error message is displayed

  Scenario: Pasting non decimal values
    Given the user selects a row in the edit forecast table
     When the user pastes non decimal values
     Then the non decimal values error message is displayed
