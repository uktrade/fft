Feature: View Admin Link on Navigation Bar

  Scenario: If users have admin access a link should be shown to the admin site
    Given I have admin site access
     When I access the FFT website
     Then I should see a link to the admin website
