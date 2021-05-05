# Headroom Studios

## Designed & Developed by Jacob Roos

## Code Institute Milestone Project 3

Headroom Studios is a site built for musicians/creatives with an added sense of community. The business provides 3 rehearsal spaces that can be rented in blocks and is supplied with all the essential equipment that would be needed (apart from the instruments).  Bookings can be made/edited on a personal profile page once the user has registered and they're also able to contribute to the noticeboard where users can post items for sale, community events and job listings!  The site was designed with a simple and intuitive layout with a focus on ensuring booking flexibility and user feedback.  A live version of the site is available [HERE](https://jacobroos87.github.io/In-a-Nutshell/).
) 

# UX

<a name="objectives"></a>

## Objectives 

* The site should attract the attention of regional musicians looking for a place to rehearse
* The facilities and ethos needs to be clear and inviting
* The process to make a booking should be simple and users should be able to check availability
* The code needs to be scalable and allow for expansion if the business grows
* Adding a post to the cummunity notice board should be simple and editable
* The user needs to come away from the site knowing what's on offer and that there is a community spirit
* The user needs to be able to sign up to a mailing list and also to contact direct for queries
* Social links and business address needs to be displayed on all pages
<a name="userstories"></a>

## User Stories 

- As a visitor to the site I want to be able to clearly see the purpose of the site and services offered
- As a visitor I'd like the navigation to be simple and easy to follow
- As a visitor I want the site to be visually appealing and have a relevant colour scheme 
- As a visitor I want to be able to see photos of the rehearsal facilities and know their cost per hour
- As a visitor I would like to be able to connect with the local community
- As a visitor I would like to be able to make bookings and check availability
- As a visitor I want to be able to edit my booking 
- As a visitor I want to be able to post on the notice board and edit that post if required
- As a visitor I want to have feedback so I know wether my booking or post has been successful
- As a returning visitor I want to be able to see my active bookings and their relative information
- As a returning visitor I want to be able to update or remove my post on the community notice board
<a name="wireframes"></a>

# Wireframes:

<a name="responsivedesign"></a>
# Responsive Design

Media queries have been added to ensure the site works well on smaller devices.  Materialize responsive classes were also used for parts of the layout.

* Home Page

The home page has a 3 column layout for 2 sections that stack for smaller devices.  The deign stays the same for tablets but collapses the navbar to a hamburger menu.

* Rehearsal Studios

The rehearsal studio page also keeps the 3 column layout and has the same principle applied for continuity.  Smaller devices stack and for tablet the design stays the same but changer the navbar to a hamburger menu.

* Notice Board

The notice board has responsive sizing so adapts to the viewport.  The posts in the notice board stay stacked with the only design change for smaller devices being the footer elements stacking which is the same for all pages.

* FAQ

The FAQ page is based around Materialize collapsible popout elements.  The design layout stays the same for all devices.  The collapsibles are in responsive containers.

* Contact

The form inside this section changes depending on the device and the text is also scaled down.

* Log In

The log in form is in a responsive container that resizes depending on the device.  I've also added media queries to extend the width for mobile devices.

* Register

The form inside the modal scales with devices and also increases in width for mobiles.

* Bookings

The bookings page has a 2 column layout that stacks for smaller devices.  The availability form has 2 inputs that are inline for larger devices and tablets but stack for mobiles.  The same priciple was applied to the lower booking form which has 3 elements that stack for mobile devices.

* Profile

The user profile page has a simle username title followed by active bookings.  For desktop devices a 3 column layout is used.  For tablets this scales down to 2 and mobiles to 1.

* New Post

The form inside this section is in a responsive container and scales for smaller devices.

* Admin (Admin only)

This admin page has the same concept as the profile pages.  Larger devices are 3 columns, tablets 2 and mobiles one.

* Log Out

The log out tab doesn't go to a separate page.  It simply logs the user out and returns them to the log in page.

# Colours & Fonts

## Colours

The colours for the site were decided based on competitor sites and also taking into consideration current colour trends. The pallette consists of a light teal green, black, wite, charcoal and a flash of orange.

The fonts all remain black and white for contrast and to improve readability.  

## Fonts

The fonts that were used on the site are "**Bungee**" and "**Roboto**".  The style of the Bungee font was inline with the slightly darker vibe and worked well as a standalone Logo font.  Roboto is a modern easy to read font that was complimentary to the bungee logo font.
[Back to top](#table-of-contents)

# Features and Structure

The site is layed out in a simple structure with smooth scrolling on the home page for the contact section and a small blurb describing the ethos of headroom studios and what facilities are available.  The Hero is consistent over all pages and has a selection of quotes from the biggest hypothetical clients that cycles through.  
All sections are focussed around a row and a 3 column layout separated with full width container sections.  The details for each page are listed below:

The main sections that were decided upon were:

* Home
* Rehearsal Studios
* Notice Board
* FAQ
* Contact
* Log In
* Register

The other sections that become available to the user once registered and logged in are:

* Bookings
* Profile
* New Post
* Admin (admin only)
* Log Out

I decided to add a user icon to the navbar with a dropdown once the user is logged in to minimise the visible tabs.  This helped to streamline the design as all of those links on one line was a bit too much!

## Navbar

* The Navbar has a Navbar brand for the website logo and 7 addition links - Home, Rehearsal Studios, Notice Board, FAQ, Contact, Log In & Register
* The Register tab links to a modal instead of a separate page.
* When logged in a user icon appears instead of log in and register. These links also become available: Bookings, Profile, Add Post, Manage Bookings (admin) & Log Out
* All the links have a hover effect and an active state when selected
* Materialize was used to create a collapsible dropdown (hamburger menu) for smaller devices that comes in from the right side of the screen

## Home

* The Home page/landing page has a hero image with a rotation of customer quotes. This functionlity was created using an interval function in JS
* Further down the page you have a small blurb about the business and what services are offered
* Underneath this there is a full width div with 6 icons highlighting the key points that make headroom studios an ideal choice for creatives
* Below this is the contact form that has a success/error modal that is displayed once the form is submitted.  Using emailJS the user is then emailed with a confirmation and the admin is sent the message that was submitted.

## Reheasal Rooms

* The page opens with a small blurb telling the user how the booking system works and includes relevant links to the sections mentioned
* Below this section I added 3 cards for the rehearsal studios with Materialize
* Each card has a small blurb about the room and its 'vibe' and includes a link to view more images
* Once the user clicks on the 'MORE IMAGES' link a modal pops up allowing the user to scroll through images of that studio
* The sizing of the images adjust depending on the device and I altered the original Materialize functionality by including prev and next arrow instead of the built in circle icons.  I decided on this due to there being quite a few images and with all the dot icons it was a bit much to navigate especially on smaller devices.

## Notice Board

* This section is made up of set of collections that are looped through and displayed with jinja/python
* The content is initially submitted through an active user which is stored on mongoDB and then brought back in with python/jinja
* There is also an if/else loop to dynamically add the category icon to the post
* The user that submits the post has to provide a contact email address which is assigned to the mail icon using jinja
* The username is also posted underneath the post title with an exclamation mark if the post was labelled as urgent
* Underneath this is a date stamp that was created using the datetime package in python and formatted using the strftime() function
* There is also pagination added with a maximum amount of posts set to 6 items before the next pages are made active

## FAQ

* The code for this page was kept simple using a Materialize collection and a set of typical questions that might be asked by users of the studio
* In terms of its design it's simple and to the point with a question answer layout
* The idea behind adding the page is purely for extra information that would be essential for a real life business!

## Contact

* The contact section contains a Materialize form with a simple opening blurb and contains 4 sections
* All sections are labelled as required and show their relevant input errors and suggestions
* A modal was added with JS and displays either a success or error message depending on the submission response
* EmailJS was used to create an email template and also an auto-reply

## Log In

* The log in page has a simple 2 section form asking for a username and password
* Python is used to then check on the mongo database if the user exists.  If the user exists they're welcomed and redirected to their profile.  If not then an error is flashed and the user is redirected back to the login page

## Register

* I decided to go for a modal for the registration to mix up the UI with something different to another page
* The modal has a 3 part form asking for a username, email and password
* This data is then stored on mongo and called upon as the 'session user' 
* The database is also checked initially on the registration and an error message is flashed if the user exists and success if the registration was a success with the user being redirected to the home page

## Bookings

* The bookings page has 2 main sections: Firstly to check availability and then to make a booking
* The section that checks availability asks the user to input a date and time. The database is then referenced using python and flashes a message saying which studio(s) are available on that date and time
* This allows for the user to make a quick check before moving ahead an filling in the main booking form
* There are required restrictions on the inputs to ensure they're filled in correctly. This functionality needed to be added seperately for the Materialize select dropdowns using JS
* The booking form then asks for date, studio, time, artist/contact name and allows a message for any special requests
* This information is stored on mongoDB and is then displayed using jinja on the user profile and also the admin page for the admin user
* Only bookings made by that user will be displayed on their profile.  I also added a sort function into the jijna loop to display the bookings in date order
* Success and error flash messages are also set up for booking confirmation

## Profile

* This is a simple page where the user can reference their active bookings and make changes or a cancellation
* The booking information is displayed in a card and includes en edit and delete icon 
* If the user wants to edit a booking the user gets transferred to a form screen that has the date and contact prefilled
* If the user tries to change to a date already booked an error is flashed and they're redirected to the bookings page where they can check availability
* Otherwise if the change is a success then the booking is updated and the changes are shown on the user profile
* If a user wants to delete a booking they simply press the delete icon which loads a confirmation modal. If the user agrees to delete then the booking is removed from the database and a confirmation flash message pops up

## New Post

* The new post page takes the user to a form that allows the user to fill in a category, title, message, email and if the post is urgent
* This information is stored on mongoDB and then looped through using jinja on the notice board page
* Once the post has been added, the user gets a confirmation flash message and the post is listed on the notice board
* This post can then be edited or deleted on the notice board page.  The delete button loads a confirmation modal and if the user chooses to delete the post it gets removed from the notice board and the database.  The edit post works in the same was as the edit booking function where the user gets taken to a form that has a some elements prefilled and then the changes are updated using the .update() function

## Admin

* This page is only available for the admin user
* It works in a similar way to the profile page but the jijna loop shows all the bookings currently in the database in date order
* The admin isn't able to edit the bookings however does have the ability to delete the bookings for potential cancellations made not via the website (hypothetically)

## Log Out

* This is a simple nav link that logs out the user using session.pop("user") and then redirects them to the log in page with a flash confirmation message

## Footer

* The footer includes a sign-up email form, address and social media links
* The sign up form puts the user email into a subscribers collection and flashes a success message.  This database can then be used by the admin for marketing purposes
* All social links have hover effects and currently link to the root websites but would be linked to the relevant pages were this a functioning business

# Future Features

The site is definitely functional however I feel that a dynamic calendar system would be advantageous and also having the ability to pay for bookings online would be ideal. I would also love to be able to implement a feature where an invoice is automatically generated and sent after a booking.  
There is also a system that I've seen used where you can send the user a code, which can then be used to unlock the studio door which would simplify the setup even more.  

* ## Known Issues

As this is a project site there are a few things that would be changed for a commercial site.  Firstly the social media links would be linked to the appropriate pages as currently these are only linked to the home pages.  The Email.js return email would be a working business email address as this is currently my own. Also there seems to be an error where the quotes that loop are displayed stacked instead of one at a time if you leave the website tab and then return.

* ## Ideas

I chose to do this as a project due to a close friend owning a rehearsal studio and this being a potential prototype to expand on.  His intention is the add recording facilities and also link to his external site which contains work of his film compositions.  

[Back to top](#table-of-contents)

# Technologies Used

## Languages

- #### HTML, CSS, JavaScript, Python

## Libraries and Frameworks

* #### [Materialize](https://materializecss.com/)
    * Used for layout, forms and navbar 
* #### [Font Awesome](https://fontawesome.com/)
    * Used for all icons
* #### [Google Fonts](https://fonts.google.com/)
    * Used for site fonts
* #### [jQuery](https://jquery.com/)
    * Used for site manipulation and to simplify JavaScript selectors
* #### [flask & Jinja](https://flask.palletsprojects.com/en/1.1.x/)
    * Used to write the backend code with python and to implement in the frontend with jinja
* #### [Email.js](https://www.emailjs.com/)
    * Used to send contact form submission data to developer and response to the user

[Back to top](#table-of-contents)