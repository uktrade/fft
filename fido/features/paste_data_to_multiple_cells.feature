Feature: Paste to multiple cells

  Scenario: When pasting into the edit forecast table, data should be changed to that of the clipboard
    Given we have entered multiple months
     When we look at last month
     Then we see last months data
