Feature: Retain forecast data entered in previous months

  Scenario: For each past month in a financial year, the last entered forecast, prior to month-close, is retained
    Given we have entered multiple months
     When we look at last month
     Then we see last months data
