Feature: Actuals and Forecast Column Headers

  Scenario: Viewing Six Months of Actuals on the Edit Forecast Page
    Given the user views the edit forecast page with six months of actuals
     When the user checks the actuals columns
     Then there are six actuals columns

  Scenario: Viewing Three Months of Actuals on the Edit Forecast Page
    Given the user views the edit forecast page with three months of actuals
     When the user checks the actuals columns
     Then there are three actuals columns
