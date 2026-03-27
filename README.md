# CityRate

## Overview  
CityRate is a web-based travel review platform that allows users to explore and share experiences about cities around the world.

Users can:
- Create an account and log in securely  
- Write reviews for cities with ratings and comments  
- Edit or delete their own reviews  
- Save drafts before publishing  
- Search for cities and browse reviews from other users  

Guest users can:
- Browse and search city reviews without logging in  

The application is built using Django, Python, HTML, CSS, and JavaScript.

---

## Setup Instructions (Local Machine)

### 1. Clone the repository
git clone https://github.com/Yara4a/CityRate.git  
cd CityRate

### 2. Create a virtual environment
python -m venv venv  
source venv/bin/activate   (Mac/Linux)  
venv\Scripts\activate      (Windows)

### 3. Install dependencies
pip install -r requirements.txt

---

## Running the Application

### 4. Apply migrations
python manage.py makemigrations  
python manage.py migrate

### 5. Run the population script
python population_script.py  

This will create sample users and review data for testing.

### 6. Start the development server
python manage.py runserver  

Open in browser:  
http://127.0.0.1:8000/

---

## Demo Login

You can log in using a demo account created by the population script:

Username: testuser1  
Password: password123  

Or create your own account using the signup page.

---

## Features

- User authentication (login/signup/logout)
- Create, edit, and delete reviews
- Draft saving functionality
- Search reviews by city
- Rating system (1–5 stars)
- User account page with personal reviews
- Responsive user interface
- JavaScript-enhanced interactions

---

## Technologies Used

- Python  
- Django  
- HTML / CSS  
- JavaScript  
- SQLite (development database)  
- PyCountry  

---

## External Sources

- Django documentation  
- PyCountry library  
- Lecture materials and online tutorials  

---

## Notes

- The database file (db.sqlite3) is not included in the repository.  
- The application can be set up using migrations and the population script.  
- Make sure all dependencies are installed before running the project.