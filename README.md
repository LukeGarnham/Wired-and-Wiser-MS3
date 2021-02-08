# Wired & Wiser

## Introduction

My website is aimed at users curious about Smart Meters.  Smart meters are electricity meters which automatically send consumption data to suppliers to allow accurate billing while providing customers with an in-home display allowing them to monitor consumption in real time.  My website provides people who are curious about smart meters with information on what they are and how they work.  My goal is to encourage visitors, both residential and commercial, to my website to book a smart meter installation with my fictional company “Wired and Wiser”.

The website allows users to sign up with a few personal details.  Once signed up and signed in, users can then book a smart meter installation by providing details of their electricity meter.  From the Account page which users see when they sign in, they can create new bookings and view, update and delete existing bookings.  They can also update and delete their account details.

This is a fictional service since in the British energy industry, customers can only request meter exchanges via their electricity supplier.  My imagined service would see my fictional company sit between customers and their suppliers where for users who book through my website, “Wired and Wiser” take on responsibility for exchanging their existing meters with a smart meter and will then inform their supplier.

My published website can be found [here](https://wired-and-wiser.herokuapp.com/).

My GitHub repository can be found [here](https://github.com/LukeGarnham/Wired-and-Wiser-MS3).

 
## UX

### User stories

I have heard about Smart Meters and I want to:
-	Find out more information about them.
-	Book smart meter installation appointments for my electricity meter(s) to be replaced with a Smart Meter(s).
-	Update my installation booking information.
-	Cancel my installation booking.
-	Change my account information including my password.
-	Delete my account.

As the website owner, I want to:
-	Inform visitors about smart meters.
-	Attract as many smart meter booking installations as possible.

### Preparation & Planning

Having worked in the energy industry, I am aware that there are many interconnected processes and chains of information passed via numerous parties.  I could have made my project a lot more complex as there are many other parts to the process of a meter installation which I could have included.  For example, if my fictitious company were real, they would have a team of qualified engineers who would need to be assigned to each meter installation booking.  Each engineer would have rotas with certain availability and cover certain regions within Britain.  These would need to be considered if users were to be given the choice to select their installation date.  Once meters are installed, the next step for my fictitious company would be to inform the supplier perhaps via an automated email being sent with information about the meter installation such as date of meter exchange, final meter read, new meter serial number.

I wanted to keep my project simple and manageable and the steps mentioned above could be future developments.  I have opted to focus on the exchange of information between customers and my fictional meter installation company, Wired and Wiser.  For this, two collections are required in my database: one for storing user information and one for storing meter installation booking information.  The users email address will act as a primary key in the *users* collection and will be used to link users to their records in the *meter_installs* collection.  I have allowed users of my website to select an installation date that suits them.  I drew the plan for my database using [app.diagrams.net](app.diagrams.net) – the plan is below:

![Database plan](static/images/readme-images/ms3-db-plan.png)

## Features

### Existing Features

#### Database
User and meter installation booking data is captured in a MongoDB database.  My database is called “wired_and_wiser”.  It contains two collections as defined above; *users* and *meter_installs*.

#### Register Form

My Register form contains 4 fields: first name, last name, email and password.  The primary key is email.  These fields are stored within my *users* collection.  The first name, last name and email address are all stored in lowercase.  The password is hashed and salted using werkzeug’s **generate_password_hash** method before being stored in the *users* collection.

Before adding a new user to the *users* collection, I check the database to see if the email address provided already exists within it.  If it does, then a flash message informs the user.  Otherwise, the user’s details are added to the *users* collection and a flash message informs them that they have successfully registered.

I added a link under the form which directs users to the sign in page.  This is in case a user tries to register but has actually already done so previously.  A flash message informs them that an account already exists with the email address they have tried to register with and so they can quickly direct themselves to the sign in page.

All fields are required before the user can submit the form.  This is indicated by an asterisk next to each form label and also in the placeholder text.  To add some further defensive design to my registration form, I applied a maximum length of 30 to the first and last name fields.  This should be sufficient for most users as I don’t think many users would require more characters.  I have also limited the first and last name inputs to just letters and a hyphen (-) for hyphenated names.  Numbers, spaces and other special characters are not required for people’s names.  I chose not to limit the length or characters in the email form.  I felt the default validation for email fields is sufficient.  For the password field, I set the minimum length as 6 and a maximum length of 15 characters.  I did not restrict the use of characters for the password field as allowing users the full choice of characters means more secure passwords can be chosen.

I inform users of the defensive design built into the form through **small** messages underneath the **input** fields which explain the requirements to pass the form validation.

The form was built utilizing various [Bootstrap form classes](https://getbootstrap.com/docs/4.5/components/forms/).  The layout is responsive; on small screens (up to 768 pixels width) the labels appear above the input fields with all text centred.  On a medium screen (768 pixels width upwards), the labels and inputs appear side by side with text justified to the left.

#### Sign In Form

The Sign In form is similar in design to the Register form.  There are two fields; one for the users email address and one for their password.  I check to see if there is a match for these two fields in the *users* database.

When the user submits the form, I first check whether the email address exists in the *users* collection.  If so, I then compare the password provided to the one stored in the database.  Since the password stored in the database has been hashed and salted, I utilize werkzeug’s **check_password_hash** method to compare the two passwords.  If they match, then the user is redirected to the Account page and a flash message appears welcoming them back.  The users email address is saved in the session variable.  If either the email address isn’t found in the *users* collection or it is but the passwords do not match, then the user is redirected back to the Sign In form (with all fields cleared) and a flash message informs that either the email address or password entered is incorrect.  Nothing gets saved in the session variable.  By not informing the user which field contains incorrect information, it makes it harder for someone trying to hack into an account as they will not know whether the email or password they’ve used is incorrect.

The form contains defensive design elements.  I have used the defensive tools provided in HTML5 rather than any custom checks besides those detailed above.  Both fields are required before the user can submit field.   There are no restrictions applied to the email address field besides the default checks performed on email inputs.  On the Register form, there is a minimum limit of 6 characters and a maximum limit of 15 characters for the password the user must provide.  In the sign in form, I decided to remove these limitations.  The reason for this is that the user will already know their password which had these restrictions applied upon creation.  The password check using werkzeug’s **check_password_hash** method validates whether the password entered matches the one provided when the user registered their account.  Unlike the Register form, I chose not to include any on-screen tips advising the user of any restrictions.

Below the form, there is a link to the Register form.  I added this in case a user accidently navigates to the sign in page when they do not have an account yet.

I have used a slightly different background image to keep the site visibly appealing although on smaller screen sizes (up to 768 pixels width), the background image is mostly hidden behind the card containing the form.

#### Account Page

When the sign in form is successfully submitted, the users email address is saved in the session variable and the Account page is loaded.  Since the Account page is dependent on the users email address being saved in session storage, I added some defensive design by including an if statement in the Python code which checks the users email address exists in session storage before the Account page is loaded.  If for any reason the users email address does not exist in session storage, the user is redirected to the Sign In page.

The Account page contains a card with a Manage Bookings tab and Manage Account tab.  Each of these views display information from the collections in my database.  The Manage Account section shows the users details from the *users* collection apart from their password which is not displayed for security reasons.  The Manage Bookings tab contains high level information about any meter installation bookings the user has and unpacks some data from the *meter_installs* collection.  This data is displayed in a table and is sorted first by install_date (starting with the earliest) and then by the first_address_line.  This is so that a user with multiple meter installation bookings (such as a business with several premises) can view them based on how soon they will be installed – if there are multiple installations on the same day they can see them listed by the first line of the address.  The information required for these tabs is passed through via two variables.

I search the *users* collection for one result using the find_one method to find one user with the users email address which is passed through to the function Python account function.  Due to the defensive design added to the Register form, there will only be one result which matches the users email address since it is the primary key.  I assign the resulting dictionary to the variable user.  Before I pass this through to the template, I remove (**pop**) the password off the dictionary.  Although the password retrieved from the collection has been hashed and salted, I felt it would improve security to not pass this through.

Next, I use the users email address to find all records in the *meter_installs* collection with the corresponding user email address.  I assign the list of results to a variable called bookings.  The results are sorted by install_date and then first_address_line.

Of course, if the user does not have any bookings then there is no data to unpack.  Therefore, before unpacking the booking data, I conduct an **if** statement using Jinja to check the length of the bookings list.  If the length of the list is greater than 0, then I unpack the data.  Otherwise, if there are no bookings (i.e. the bookings list length is 0), I display a message to the user advising them that “You don't currently have any meter installations booked.”.

For the bookings data, I opted to only display a small amount of information on screen.  The reason is that there is a lot of information for each booking and for users with multiple bookings, there would be a lot of information to display on screen.  Instead, I deemed that the first line of the address, postcode, meter ID and installation date would be the key pieces of high-level information to display on this screen.  On small and medium screens (up to 992 pixels width), the postcode and meter ID columns are not displayed.  Even then, not all of the information can be seen on smaller screens so there is a horizontal scroll so users can still see all of the information rather than it spilling over.

As well as unpacking the bookings data on the page, I also opted to display the number of bookings next to the tab title using the length method to improve user experience.

I also included two links for each booking; one to view the booking and one to edit the booking.  On small screens, only an icon is shown but on medium screens (786 pixels width upwards), text appears alongside the icon.  This is to save horizontal space on smaller screens.

On the Manage Account tab, I display the users first name, last name and email address.  I include links here for the user to Update Details on their account and to Delete Account.

Lastly, I decided to swap the styles for the active and not active tabs around.  The original styles inherited from Bootstrap had the active tab with a light grey background colour and the inactive tab with a black background colour.  This was the inverse of the effect on the header navbar.  Furthermore, I also felt that this made the active tab look inactive and vice versa which as I was testing did not feel like a good user experience.  Using the Google Chrome inspection tools, I copied the Bootstrap rules and placed them in my CSS file.  I then swapped the styles around between the two rules thus inverting the styles.  I also added a hover effect to the inactive tab so that the text appears in orange – this is a style applied throughout my website and I wanted to include it on the tabs here too.

#### Book Smart Meter Installation Page

There are multiple fields on the booking page.  Below is a summary of each:

**Meter ID**:  This field is required, and it is restricted to numbers only.  The meter ID should be 13 digits long so there is a minimum and maximum length of 13 applied to restrict users submitting anything other than 13 numbers.  A small note beneath the field informs users of this.  Each supply point has a unique meter ID which is why as an installer, I need this number.  I have provided an info icon which launches a modal to explain to users what the meter ID is and where they can find it.

**Meter Serial Number**:  This is not a required field.  I have applied a maximum length of 12 characters because although there is no fixed length for a meter serial number, they are not longer than this.  The meter serial number is not necessarily unique but would be nice to know as the installer hence why I have included the field but not made it a required field.  I have provided an info icon which launches a modal to explain to users what the meter serial number is and where they can find it.

**Address**:  The address is split into 6 inputs to reflect each line of a user’s address.  The first line, town, county and postcode are all required fields.  For all fields except the postcode, I imposed a maximum limit of 50 characters.  I felt that this should prevent malicious users submitting spurious information to my database whilst providing users with enough characters to detail their address properly.  For the postcode, I imposed a minimum length of 6 and a maximum length of 8 characters since all UK postcodes fall into this range (including the space in the middle).

**Meter Location**:  This is a text-area field with no restrictions applied to the user input.  It is a required field because the installer will need to know where in the property the meter is located.

**Access Instructions**:  This is a text-area field with no restrictions applied to the user input.  This is not required but allows users to provide some additional information about accessing the property which may be useful to me as the company installing the meter.

**Parking**:  This is a required field and is simply a select input giving users the choice of yes or no.

**Property Type**:  This is also a required field requiring the user to select either residential or commercial.

**Supplier**:  This is a required field.  I considered making this a select list as well.  However, suppliers are constantly entering and exiting the market place so it would become a separate task in itself to keep this list updated.  Therefore, I left it as a text field for users to populate.  I only want the supply company’s name so I thought it would be beneficial to cap the amount of characters a user can input into this field.  Therefore, I have applied a maximum length of 30 characters.  As the installation company, I will need to liaise with the supplier to notify them on the meter being replaced.

**Account Number**:  It would be beneficial to me to know the supplier account number when I inform the supplier that my company has been contacted to replace the meter for the user.  As something that would be nice to have but not essential, the field is not required.  Account numbers can contain letters so I chose not to restrict the characters users can input.  I applied a maximum length of 20 which will be sufficient for an account number; whilst they can vary in length, they are typically no more than 12 characters.

**Meter Reads**:  I have provided two fields for the users to submit meter reads.  This is because meters typically have either one register for consumption 24/7 or two registers; one for day and one for night-time usage.  Neither of these fields are essential which is why they are not required.  If the user does provide them, I can pass them onto the supplier to ensure their bills are accurate.  Meter registers are typically 6 digits long however, I have provided a maximum length of 8 characters just in case a user has a meter with more digits than usual.  I have restricted the input to only numbers.

**Installation Date**:  This field is required as I need to know when the user wants their meter installed.  Using jQuery UI and jQuery, I set up this input field to have a calendar appear when the user clicks or tabs into this input field.  I chose a jQuery UI theme (darkness) which closely matches the colour scheme of my website.  I linked to the version 1.12.1 darkness theme CSS theme using a CDN I found on [this website](https://cdnjs.com/libraries/jqueryui).  I linked to the jQuery UI version 1.12.1 JavaScript files via a CDN also found on [this website](https://code.jquery.com/).  Using the built in [jQuery UI options](https://api.jqueryui.com/datepicker/), I set up the earliest install date to be 30 days from today’s date.  This is because as an installation company, I need time to plan my workload and cannot have users booking in a meter installation at 24 hours’ notice.  I also restricted users from selecting a date beyond 2 years into the future since I wanted to impose an upper limit to the range of time we can take bookings.  I also restricted installations from being booked on a Sunday to reflect the business opening hours.  I used the jQuery UI options but referred to [this solution](https://stackoverflow.com/questions/31770976/disable-specific-days-in-jquery-ui-datepicker) I found online.

**Authorisation**:  The last part of the form is a checkbox asking the user to authorise Wired & Wiser to complete the installation and to contact their supplier.  As a meter installed, I need to liaise with the supplier to inform them of the new meter details and pass on final meter reads from the old meter to maintain accurate billing for the customer.  Due to GDPR, I need some form of authorisation to speak to the supplier on behalf of the customer.  This checkbox acts as that authorisation.  Without this authorisation, my company cannot install the new smart meter.  Therefore, using jQuery I prevent the user from submitting the form unless this checkbox is checked/ticked.  This means that all bookings I receive will have this authorisation granted.  If a user doesn’t give this consent then they cannot complete the booking.

When the form is submitted, the record is added to the *meter_installs* collection.  However, I first check to see if there is an existing record in the collection with the same meter ID.  Whilst the “_id” field is the unique and primary key, I also want the meter ID to be unique in my collection.  The reason for this is that the meter ID acts as a unique identifier of each meter point in the electricity industry.  As a meter installation company, I don’t want to have two bookings for the same meter ID.  If someone tries to enter a record with a meter ID which already exists in my collection, a flash message informs them and the record is not inserted in my collection.

#### View Booking Page

From the Account page, under Manage Bookings, users can click the View button.  The View Booking page shows all information related to a particular booking.  The page template takes a unique booking ID as an argument.  The entirety of the booking details are retrieved from the *meter_installs* collection and this is passed through to the template.  The template unpacks this date onto the page using Jinja next to corresponding labels.  Dates are formatted to “dd/mm/yyyy” strings.  The parking_on_site and property_type are capitalised to improve the visual look. 

The page contains 3 options; Update Booking, Delete Booking or return Back To Account.  Before the booking is deleted, a modal fades in asking the user to confirm whether they want to proceed.  I included this to improve user experience; I didn’t want a user to accidentally click the delete booking and have no chance to rectify this prior to the booking being cancelled.

When a user confirms they want to cancel their booking, the delete_booking function is called.  The (python) delete_booking function takes the booking ID as its only argument.  Since the booking ID is unique, I use the delete_one method to delete the record with the corresponding booking ID.  A flash message informs the user that their booking has been successful and they are redirected to the Account page.

#### Update Booking Page

The Update Booking page was initially a copy of the booking page.  In here I unpack the data into the form using the **value** attribute in most cases.  For required fields, I know that a record would exist in my *meter_installs* collection so I unpack it as the **value** in the field.  However, for the fields which aren’t required, I used **if** statements to either display the value retrieved from the *meter_installs* collection if there is one or where there isn't, placeholder text.

Users are free to update all fields that appear on the booking form.  The required fields remain the same and the user must once again tick the authorisation checkbox before they can submit their changes.  The data validation rules imposed on this form mirror those from the Booking form.

The installation date can be left as it is but if the user wants to edit it, then they must give 30 days’ notice once more.  I have updated the note underneath the field to inform users of this.

When the form is submitted, I check once more to ensure that there are no other bookings in the *meter_installs* collection.  This is in case the user has updated the meter ID.  I want to ensure that the meter ID is unique within my collection since they are a unique identifier used within the electricity industry.

The application date is not updated when a booking is updated.  Instead, I decided that the original application date should be maintained.

I have also included an option for users to delete the booking.  As with the View Booking page, there is a modal which ensures users must click twice to say they want to delete a booking.  This helps prevent bookings from being deleted accidentally.

There is also a button which enables users to return to the account screen.

#### Update Account Page

The Update Account page was originally a copy of the Registration page.  The users account details are retrieved from the "users” collection and passed through however for security reasons I remove (**pop**) the password off beforehand even though it has been hashed.  The form field **placeholders** have been replaced with the **values** of the first name, last name and user email address retrieved from the *users* collection.  This allows users to amend these fields.  The password field still contains the original **placeholder** but I have changed the note underneath informing users that in order to update their details, they must submit their current password.  The same defensive design is applied to all fields as in the Registration page.

When the form is submitted (POST method), I check that the password matches the existing password using the werkzeug’s **check_password_hash** method.  If not, the user is redirected back to the Update Account page with a flash message informing them that the password they entered is incorrect.  Otherwise, I create a dictionary called update_user and assign the form values to keys with the exception of the password key to which I assign the existing password.

Next I check to see whether the user has updated their email address.  If so, then I check to see whether the new email address the user has submitted already exists in my *users* collection.  I don’t want users to be able to change their email address to one which already exists in the users collection.  If there is already a record with the new user email address a user has submitted, a flash message informs them and they are redirected to Update Account page.

Otherwise, if they have changed their email address to one which still remains unique within the *users* collect, there are two extra steps I need to take.  Since all meter installation bookings in the *meter_installs* collection contain the users original email address, I need to update this field.  If I don’t do this, then the Account page will not return/show any bookings they have made.  By referring to [this webpage](https://www.w3schools.com/python/python_mongodb_update.asp), I use the **update_many** method to update all meter install records which have the users old email address in the user_email_address field.  I then update them with the new email address using the **$set** method.  Secondly, I also update the user email address that is saved in session storage.

Regardless of whether the users email address has changed or not, I then use the **update** method to find a record in the *users* collection with the users unique id and update the record to the update_user dictionary.  I could have used the users original email address to find their unique record in the *users* collection but decided it would be better practice to use the id.

Once the form is successfully submitted, I redirect the user back to the Account page and display a flash message informing them that their account details have been updated.  They can then see their updated account details by checking the Manage Account tab.

#### Delete Account

From both the Account and Update Account pages, I have included a Delete Account button.  This initially launches a modal since I don’t want users to accidentally click this and have their account deleted.  In the modal, as an added layer of defensive design, the user must enter their password before confirming that they want to delete their account.

When the user does this, the (Python) delete_account function is called.  This uses werkzeug’s **check_password_hash** method to check that the password entered by the user matches the hashed one stored in the *users* collection.  If not, then the user is returned to the Account page and a flash message informs them that the password they have entered is incorrect.  If the user enters the correct password, then it deletes both the users record in the *users* collection and all bookings in the *meter_installs* collection with the users email address.  Since there could be multiple bookings made by the user, I use the **delete_many** method which I read about on [this website](https://www.w3schools.com/python/python_mongodb_delete.asp).  To delete the user from the *users* collection, I use the **delete_one** method and use the users id to find and delete the correct record.  I could have used the users email address since this is also unique in the *users* collection but opted to use the id.  Finally, I also remove the users email address from session storage.  The user is then directed back to the Register page.

### Features Left to Implement






## Technologies Used

### Bootstrap & Bootswatch

[Bootswatch](https://bootswatch.com/) has a number of themes which are built upon the Bootstrap library.  I chose the theme call [slate](https://bootswatch.com/slate/) as a basis for my project.  The theme has a strong dark colour palette based around the hex colour #272b30.  At the time I started my project, Bootstrap v5.0 had just been released.  However, the latest version the Bootswatch themes were built for was Bootstrap v4.5.3.  To avoid any possible conflicts, I opted to use [Bootstrap v4.5](https://getbootstrap.com/docs/4.5/getting-started/introduction/) in my project.

![Bootswatch versions](static/images/readme-images/bootswatch-versions.png)

Rather than use the Bootstrap CDN link, I used the [Bootswatch link](https://www.bootstrapcdn.com/bootswatch/) for the slate theme.  This is placed in the **head** element of my base.html file.

### jQuery

I used jQuery to help write bespoke JavaScript code.  I used the latest version available; version 3.5.1 which can be found [here](https://code.jquery.com/).  The uncompressed CDN link is placed in the bottom of the body in the base.html template thus it is extended to all other pages.  I used this for the datepicker widget on the Booking form and Update Details form.

### jQuery UI

I used the [jQuery UI library](https://code.jquery.com/) to import the ui-darkness theme.  Rather than download the CSS file for the theme, I imported it via a CDN link in the **head** element of the base.html file.  I found the CDN link for the ui-darkness/jquery-ui.min.css file [here](https://cdnjs.com/libraries/jqueryui).  I did this to style the datepicker widget on the Booking form and Update Details form.

### FontAwesome

I used [Font Awesome](https://fontawesome.com/start) to provide icons throughout my project to improve UX.  The CDN link for Font Awesome in the **head** element of my base template.

### Google Fonts

I imported two fonts from [Google Fonts](https://fonts.google.com/) to overwrite the Bootswatch fonts.  I imported [Open Sans](https://fonts.google.com/specimen/Open+Sans) which I applied to the body and [Noto Sans JP](https://fonts.google.com/specimen/Open+Sans) which I applied to headers.

## Testing

### Bugs / Problems Encountered During Development

#### NavBar

The original code for my **nav** element was copied from [Bootstrap](https://getbootstrap.com/docs/4.5/components/navbar/#toggler).  I modified this code to achieve the final result present in my project.  The first change I made was to keep the background colour consistent with the slate background colour in the body.  I made the text white as well to ensure strong contrast between text and background colour.  These changes were achieved simply by removing the “navbar-light” and “bg-light” Bootstrap class names from the **nav** element.  This created a problem with the navbar toggler icon; the default icon image did not contrast well with the slate background: 

![Navbar toggle icon not very visible](static/images/readme-images/toggle-icon-1.png)

To resolve this I replaced the Bootstrap navbar-toggler-icon with the [Font Awesome bars](https://fontawesome.com/icons/bars?style=solid) icon.  I applied white font and also a white border to the toggle icon.  Finally I wrote some custom CSS to apply a white border to the bottom to achieve this final result:

![Navbar toggle icon now fixed](static/images/readme-images/toggle-icon-2.png)

When setting up the links in the navbar, I wanted to have some links which appear as call to action buttons on the right side on large screens.  To achieve this I used the [Bootstrap display properties](https://getbootstrap.com/docs/4.5/utilities/display/) so that the call to action buttons are hidden until the screen size is large (992 pixels width upwards) at which point the navigation links are hidden from the unordered list in the collapsible navigation menu.  This results in the following view on screen sizes up to 992 pixels wide:

![Navigation links on small & medium screens](static/images/readme-images/navigation-links-1.png)

And this was the result on large screen sizes (992 pixels width upwards):

![Navigation links on larger screens](static/images/readme-images/navigation-links-2.png)




In this section, you need to convince the assessor that you have conducted enough testing to legitimately believe that the site works well. Essentially, in this part you will want to go over all of your user stories from the UX section and ensure that they all work as intended, with the project providing an easy and straightforward way for the users to achieve their goals.

Whenever it is feasible, prefer to automate your tests, and if you've done so, provide a brief explanation of your approach, link to the test file(s) and explain how to run them.

For any scenarios that have not been automated, test the user stories manually and provide as much detail as is relevant. A particularly useful form for describing your testing process is via scenarios, such as:

1. Contact form:
    1. Go to the "Contact Us" page
    2. Try to submit the empty form and verify that an error message about the required fields appears
    3. Try to submit the form with an invalid email address and verify that a relevant error message appears
    4. Try to submit the form with all inputs valid and verify that a success message appears.

In addition, you should mention in this section how your project looks and works on different browsers and screen sizes.

You should also mention in this section any interesting bugs or problems you discovered during your testing, even if you haven't addressed them yet.

If this section grows too long, you may want to split it off into a separate file and link to it from here.

## Deployment

This section should describe the process you went through to deploy the project to a hosting platform (e.g. GitHub Pages or Heroku).

In particular, you should provide all details of the differences between the deployed version and the development version, if any, including:
- Different values for environment variables (Heroku Config Vars)?
- Different configuration files?
- Separate git branch?

In addition, if it is not obvious, you should also describe how to run your code locally.


## Credits

### Content
- The text for section Y was copied from the [Wikipedia article Z](https://en.wikipedia.org/wiki/Z)

### Media
- The photos used in this site were obtained from ...

### Acknowledgements

- I received inspiration for this project from X