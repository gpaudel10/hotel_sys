
## Hotel Reservation System 

**Task Title**: Build the Room Availability and Booking Module for a Hotel Reservation System 
**Description**: 
Your task is to develop a module that allows users to check room availability and 
make bookings. 
The module should include the following functionalities: 

**Authentication:** 
○  Implement a basic login system for users. 
○  Allow users to view and cancel their bookings. 
A functioning module that handles room availability and booking. 
Documentation explaining how the module works and how to set it up. 

**Check Room Availability:** 
○  Users should be able to select check-in and check-out dates. 
○  Based on the selected dates, the system should display available rooms 
categorized by type (e.g., single, double, suite). 

**Booking Functionality:** 
○  Enable users to select a room and proceed with the booking. 
○  Collect necessary user information (e.g., name, contact details, payment details). 
Data Storage: 
○  Use a database PostgresSQL to store room details, 
availability, and booking records


### This is the Project Structure

│
├── app/
│   ├── __init__.py
│   ├── auth/
│   │   ├── __init__.py
│   │   ├── routes.py
│   │   └── models.py
│   ├── booking/
│   │   ├── __init__.py
│   │   ├── routes.py
│   │   └── models.py
│   ├── templates/
│   │   ├── auth/
│   │   │   ├── login.html
│   │   │   └── register.html
│   │   └── booking/
│   │       ├── index.html
│   │       ├── availability.html
│   │       └── booking_form.html
│   
├── config.py
├── requirements.txt
└── run.py
├── init_db.py


Here's a general overview from each section (what is it and how does it work?):

*app/ Directory:*

This is the main application directory. It contains subdirectories for authentication (auth/) and booking (booking/)

*app/auth/ Directory:* 

This directory contains the authentication routes and models. It includes routes for login, registration, and logout. 
It has an __init__.py file to initialize the blueprint and a routes.py file for defining the routes and models.py file for defining the models related to authentication. 
- routes for /login, /register, and /logout.
- logic for user authentication and session management.
- Hash passwords using werkzeug.security..
- implement password validation (such as  minimum length, special characters).

*app/booking/ Directory:*

This directory contains the booking routes and models. It includes routes for availability and booking. 
It has an __init__.py file to initialize the blueprint and a routes.py file for defining the routes and models.py file for defining the models related to booking.


*templates/ Directory:*

This directory contains the HTML templates for rendering views. It includes a login.html, register.html, index.html, availability.html, and booking_form.html.

*app/__init__.py:*  

This file is essential for initializing the flask application. It imports required modules and sets up the application object. it has login_manager and db objects. This file is typically used to initialize the Flask application and configure extensions (e.g., database, login manager).

- flask app initialization.
- database configuration.
- blueprint registration (for auth and booking modules).

*config.py:*
It solves the database configuration. It has database credentials and secret keys and also i will generates if not present.

*init_db.py:*
this file is used to initialize the database schema as well as initialize the data as well.

*requirements.txt:*

This file contains all the required packages and their versions and dependencies.

*run.py:*

this is the main file to run the application. It imports the create_app function from the app package.



### Process to run the application

at first initialize the database using:

```bash
python init_db.py
```

then run the application using:

```bash     
python run.py  

```