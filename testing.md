## Testing

### Tools
The following tools were used to test the website code and layout throughout the development.

* Google Chrome Developer Tool - used throughout the project to test code and scalability.
* Unicorn Revealer - used throughout the project to resolve layout issues with web pages.
* Contrast Ratio - used to ensure that colours meet readability guidelines.
* W3C Markup Validation - used to validate HTML code.
* W3C CSS Validation - used to validate CSS code.
* JS Hint - used to validate JS code
* Pylint - to validate Python code.

### User Testing 

#### All Pages 

* Header
    1. Click on the RCN logo to verify it links to user's home page when logged in and the login page when not logged in. 
    2. Hover over the navigation burger to check that the button changes from blue to purple.
    3. Click on the navigation burger to ensure that the navigation bar drops down.
    4. Click on the navigation burger again to check that it retracts.
    5. When user is not logged in, check that navigation bar shows only login and signup.
    6. When member is logged in, check that nav bar shows logout, home page, update account details, ask new question.
    7. When user is logged in, check that nav bar shows logout, home page, update account details, unassigned questions and member accounts.
    8. Click on each navigation option to ensure that they navigate to the appropriate pages or carry out the appropriate actions.

* Footer
    1. Click on each link to check that they link to the appropriate pages and open in a new page.

* Text and grid design
    1. Change the screen resolution to ensure that text and grid layout react as expected on all screen sizes. All text should be readable, images should not be distorted and pages should not be cluttered.

#### Login 
* Login Form 
    1. Try to submit without email or password input. Message should appear to state that fields need to be filled.
    2. Try to submit with an email input that doesn't follow email format. Error message should display to state invalid email address.
    3. Try to submit with email address but no password. Flash message should state invalid email/password combination.
    4. Submit with email address and incorrect password. Flash message should state invalid email/password combination.
    5. Submit with valid email and password combination. User should be redirected to their home page and flash message should confirm successful login to suitable type of account (ie member or staff).
    6. Click on Sign Up link to check that it directs to Sign Up page.

* Responsive grid 
    1. Check that login fields expand and screen sizes increase. Should remain full width of screen. 

#### Sign Up 
* Member/Staff Sign Up Forms
    1. Try to submit without any fields completed. Message should appear to state that fields need to be filled. 
    2. Try to submit with some fields completed but leave first name, last name, email, password or confirm password blank. Message should appear to state that fields need to be filled.
    3. Try to submit completed form but confirm password does not match password. Error message should state passwords must match.
    4. Submit after entering an email input that does not include @. Error message should state invalid email address.
    5. Submit with an email address that is already on the mailing list. A flash message should appear to inform user that the email address is already registered and invite user to login instead.
    6. Attempt to enter letters into the telephone field. Should not be able to do so.
    7. Enter a number with less than 11 digits into telephone field. An error message should state that telephone number needs to be 11 digits long.
    8. Press submit after completing all required fields and entering a new email address. User should be redirected to their user home page and a flash message confirms that the appropriate type of account has been created.
    9. Client checks MongoDB to ensure that all the appropriate information has been sent to the database.

* Responsive Grids 
    1. Form should display as one column in smaller screens and over two columns in larger screens. 

#### Home Page (Staff User)
* Task buttons 
    1. Check that buttons are those intended for staff; update account, assigned questions, unassigned questions, all member accounts.
    2. Hover over buttons to ensure that they change from blue to purple. 
    3. Click on assigned questions button, should scroll page to questions container.
    4. All other buttons should redirect to the suitable page. 

* Account Details 
    1. Account information should correspond with user's details. 
    2. Should display workplace, not employer.

* Assigned Questions 
    1. Click on each tab.
    2. If there are no questions to user, nothing should appear.
    3. Check that questions with no end date appear in current tab.
    4. Check that questions with an end date appear in closed tab. 
    5. Check that questions show in start date order, most recent at top. 
    6. Click on summary button, should expand to show question summary.
    7. Full Details button should redirect user to Staff Question Details page.

* Responsive Grid 
    1. On smaller screens containers should display in one column.
    2. On larger screens, first two containers should show display side by side, equal sizes. Container three should be full width. 

#### Home Page (Member View)
* Task Buttons 
    1. Check that buttons are those intended for a member; update account details, ask question, see current/closed questions.
    2. Hover over buttons to ensure that they change from blue to purple. 
    3. Click on current/closed questions button, should scroll page to questions container.
    4. All other buttons should redirect to the suitable page. 

* Account Details 
    1. Account information should correspond with user's details. 
    2. Should display employer, not workplace.

* Current/Closed Questions 
    1. Click on each tab.
    2. If there are no questions to user, nothing should appear.
    3. Check that questions with no end date appear in current tab.
    4. Check that questions with an end date appear in closed tab. 
    5. Check that questions show in start date order, most recent at top. 
    6. Click on summary button, should expand to show question summary.
    7. Full Details button should redirect user to Member Question Details page.

* Responsive Grid 
    1. On smaller screens containers should display in one column.
    2. On larger screens, first two containers should show display side by side, equal sizes. Container three should be full width. 

#### Account Details 
* Account Form 
    1. Cannot alter username.
    2. Check that prepopulated information relates to user.
    3. For members, employer should show. For staff, workplace should show with select options.
    4. Try to submit without any fields completed. Message should appear to state that fields need to be filled. 
    5. Try to submit with some fields completed but leave email blank. Message should appear to state that fields need to be filled.
    6. Try to submit completed form but confirm password does not match password. Error message should state passwords must match.
    7. Submit after entering an email input that does not include @. Error message should state invalid email address.
    8. Attempt to enter letters into the telephone field. Should not be able to do so.
    9. Enter a number with less than 11 digits into telephone field. An error message should state that telephone number needs to be 11 digits long.
    10. Press submit after completing all required fields. User should be redirected to their user home page and a flash message confirms that the account has been updated.
    11. Check the home page account details to ensure that account details have been updated.
    12. Client checks MongoDB to ensure that all the appropriate information has been sent to the database.

* Breadcrumbs
    1. Check that links direct to the appropriate pages for the user.

* Responsive Grid 
    1. For smaller screens, labels and inputs should show as one column.
    2. For larger screens, form should be displayed in centre of screen and labels side by side with inputs.

#### New Question
* Form 
    1. Must select option from dropdown for question type. 
    2. Data required in the question details. 
    3. Once successfully submitted, user redirected to home page and flash message confirms that question has been submitted.

* Breadcrumbs 
    1. All links lead to the appropriate pages for the user.

* Responsive Grid 
    1. For smaller screens, labels and inputs should show as one column.
    2. For larger screens, form should be displayed in centre of screen and labels side by side with inputs.

#### Question Details - Member
* RCN Lead 
    1. If RCN Lead not assigned, general message with contact details should display.
    2. If RCN Lead assigned, check that appropriate contact details display. 
    3. Contact RCN Lead button should change from blue to purple when hovered over.
    4. Check button links to appropriate page. 

* Question Details 
    1. Check that question details match the question.
    2. Check that dates are in suitable format.
    3. If question open, no end date should display. If closed, end date should appear. 

* Contacts
    1. If there are no contacts related to question, nothing should appear.
    2. Check that contacts show in date order, most recent at top. 
    3. Click on details button, should expand to show contact details.
    4. Edit button should appear only for contacts created by the user.
    5. Check that edit button directs to suitable page.

* Breadcrumbs
    1. Check that links direct to the appropriate pages for the user.

* Responsive Grid 
    1. On smaller screens containers should display in one column.
    2. On larger screens, first two containers should show display side by side, equal sizes. Container three should be full width. 

#### Question Details - Staff 
* Task Buttons 
    1. Hover over buttons to ensure that they change from blue to purple. 
    2. Click on browse contacts button, should scroll page to contacts container.
    3. Assign question and close question buttons should display modal.
    4. All other buttons should redirect to the suitable page. 

* Assign Modal 
    1. Check that all staff are select options and unassigned is also an option.
    2. Check that modal closes when clicked outside the modal box.
    3. Check that X button closes the modal.
    4. Check that submit button assigns the question to the appropriate staff.

* Close Modal 
    1. Check that modal closes when clicked outside the modal box.
    2. Check that X button closes the modal.
    3. Check that button closes question and end date appears in question details.

* Question Details 
    1. Check that details match question data. 
    2. End date should be empty if question open. End date should display if question closed. 

* Member Details 
    1. Check that member details match appropriate member. 

* Contacts
    1. If there are no contacts related to question, nothing should appear.
    2. Check that contacts show in date order, most recent at top. 
    3. Click on details button, should expand to show contact details.
    4. Edit button should appear only for contacts created by the user.
    5. Check that edit button directs to suitable page.

* Breadcrumbs
    1. Check that links direct to the appropriate pages for the user.

* Responsive Grid 
    1. On smaller screens containers should display in one column.
    2. On larger screens, first container should show full width, second and third containers should show display side by side, equal sizes. Container four should be full width. 

#### Contact Form 
* Form 
    1. From and To inputs should be read only.
    2. From should display user's name.
    3. If staff, To should display member who asked question.
    4. If member, To should display RCN Lead. If no RCN Lead assigned, should display "RCN".
    5. If try to submit with question details empty, message appears to state that field cannot be empty.
    6. If member, once successfully submitted, redirected to Member Question Details and success flash message appears.
    7. If staff, once successfully submitted, should be redirected to Staff Question Details and success flash message appears.

* Breadcrumbs 
    1. Check that all links direct to appropriate site for user.

* Responsive Grid 
    1. For smaller screens, labels and inputs should show as one column.
    2. For larger screens, form should be displayed in centre of screen and labels side by side with inputs.

#### Detailed Contact Form 
* Form
    1. Check that From input has prepopulated value of user's name. 
    2. Make sure this can be altered.
    3. Check that date is prepopulated with current date and time.
    4. Check that can only submit date in specified format.
    5. Check that cannot submit form without contact details input.
    6. Once submitted, member should be redirected to Member Question Details and staff should be redirected to Staff Question Details. Success flash message should appear.

* Breadcrumbs 
    1. Check that all links direct to appropriate site for user.

* Responsive Grid 
    1. For smaller screens, labels and inputs should show as one column.
    2. For larger screens, form should be displayed in centre of screen and labels side by side with inputs.

#### Unassigned Questions 
* Accordions 
    1. Check that accordions open to display question summary.
    2. Check that more than one accordion can be open at a time.
    3. Check that questions display in start date order, earliest at the top. 
    4. Client can check database to ensure that all unassigned questions appear. 
    5. Check that full details redirects to appropriate Staff Question Details page for that question. 
    6. Check that assign question button displays modal. 

* Assign Modal 
    1. Check that all staff are select options and unassigned is also an option.
    2. Check that modal closes when clicked outside the modal box.
    3. Check that X button closes the modal.
    4. Check that submit button assigns the question to the appropriate staff.

* Breadcrumbs 
    1. Check that all links direct to appropriate site for user.

* Responsive Grid 
    1. Check that accordion remains full width at all screen sizes. 
    2. Check that accordion information is easily readable in all screen sizes.

#### All Member Accounts 
* Member List 
    1. Client can check with database that all member users are listed.
    2. Members should display in alphabetical order, according to their last name. 
    3. Button should direct to appropriate Staff Member Details page for that member.

* Search Bar 
    1. Try to search with name, job title and employer. Ensure that results are accurate. 
    2. Delete search input to ensure that full list reappears. 

* Breadcrumbs 
    1. Check that home page directs to user's home page. 

* Responsive Grid 
    1. On smaller screens, member name, job title and employer should be listed and labels appear.
    2. On larger screens, details show in a table format with titles for each column.

#### Member Account Details - Staff View 
* Member's Account Details 
    1. Check that details correspond to the member and all information displays. 

* Member's Questions
    1. If the member has not asked any questions, nothing should appear.
    2. Check that questions show in start date order, most recent at top. 
    3. Click on summary button, should expand to show question summary.
    4. Full Details button should redirect user to appropriate Staff Question Details page.

* Breadcrumbs 
    1. Check that all links direct to appropriate site for user.

* Responsive Grid 
    1. On smaller screens, containers should be in one column whole width of screen.
    2. On larger screens, container one should be half the width of the screen and contianer two should be whole width.

### User Feedback
Friends, family and colleagues were enlisted to test the site on mobile phones, tablets, laptops and desktops. They also tested the site using different bandwidths to ensure that the there were no significant loading time lags.

The following changes were made in response to user feedback:
* Some button and form inputs were relabelled to make clear what was expected of the user.
* Additional padding was added to some areas, to make more readable on smaller screen sizes.

### Problem Solving 
User testing was carried out throughout the project, which indentified some bugs or potential problems.
* It was recognised that using an email address as the session identifier for the user may not be best security practice. Since authentication was not the focus of this project, it was decided that changing this was not a priority but learning would be done for future projects.
* The Date Time Picker initially used for some of the forms was not compatible with some web browsers, so was removed. Alternatives attempted, such as JQuery, caused interference with other parts of the site so were dropped from the final project. 
* Although it should not be possible for a user to be logged in as neither member or staff, failsafes were put into the methods to throw an error message if this did occur. 
