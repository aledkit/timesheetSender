# timesheetSender
  
Simple python script to make sending timesheets easier  
  
On run opens GUI to input hours into a table  
User input is formatted into a HTML table and sent to email recipient  
  
secrets.json must be updated to function properly  
  - sender_email - your email (use gmail)  
  - sender_password - app password generated through gmail  
  - recipient_email - email sent to when DEBUG = False  
  - test_email - emailsent to when DEBUG = True

DEBUG is true by default
