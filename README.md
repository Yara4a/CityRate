# CityRate 🌍

CityRate is a Django-based web application that allows users to share and explore reviews of cities around the world. Users can create, edit, and manage their own reviews, rate cities, and browse feedback from other users.

---

## 🚀 Features

- User authentication (Sign up, Login, Logout)
- Create, edit, and delete reviews
- Save drafts before publishing
- Star rating system (1–5)
- Search reviews by city
- Personal account page for managing posts
- Public review feed
- Responsive design using Bootstrap and custom CSS

---

## 🛠️ Technologies Used

- Python (Django)
- HTML, CSS, JavaScript
- Bootstrap (responsive framework)
- SQLite (development database)

---

## ⚙️ Installation & Setup

Follow these steps to run the project locally:

### 1. Clone the repository

```bash
git clone https://github.com/Yara4a/CityRate.git
cd CityRate
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Apply migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 4. Populate the database

```bash
python import_cities.py
python population_script.py
```

### 5. Run the server

```bash
python manage.py runserver
```

### 6. Open in browser

http://127.0.0.1:8000/

---

## 👤 How to Use

1. Create an account or log in  
2. Write a review for a city  
3. Save it as a draft or publish it  
4. Edit or delete your reviews from your account page  
5. Browse and search reviews from other users  

---

## 🧪 Testing

Run the test suite using:

```bash
python manage.py test
```

Tests cover:
- User authentication
- Review creation and validation
- Permissions (edit/delete)
- Core view functionality

---

## 📁 Project Structure

```
CityRate/
├── city/                  # Main Django app
├── templates/             # HTML templates
├── static/                # CSS, JS, images
├── population_script.py   # Generates sample data
├── import_cities.py       # Imports city dataset
├── requirements.txt
└── manage.py
```

---

## 📌 Notes

- The database file (`db.sqlite3`) is not included and will be generated after running migrations.
- The population script creates realistic sample data for demonstration.
- All JavaScript and CSS are stored in static files (no inline code).

---

## 🌐 Deployment

This project is designed to be deployable on PythonAnywhere.

---

## 👥 Team

- Sable  
- Yara  
- Abdullah  
- Rabindra  

---

## 📚 External Resources

- Bootstrap — https://getbootstrap.com/  
- Google Fonts — https://fonts.google.com/  
- Django Documentation — https://docs.djangoproject.com/  

---

## 📄 License

This project was developed for educational purposes.# CityRate 🌍

CityRate is a Django-based web application that allows users to share and explore reviews of cities around the world. Users can create, edit, and manage their own reviews, rate cities, and browse feedback from other users.

---

## 🚀 Features

- User authentication (Sign up, Login, Logout)
- Create, edit, and delete reviews
- Save drafts before publishing
- Star rating system (1–5)
- Search reviews by city
- Personal account page for managing posts
- Public review feed
- Responsive design using Bootstrap and custom CSS

---

## 🛠️ Technologies Used

- Python (Django)
- HTML, CSS, JavaScript
- Bootstrap (responsive framework)
- SQLite (development database)

---

## ⚙️ Installation & Setup

Follow these steps to run the project locally:

### 1. Clone the repository

```bash
git clone https://github.com/Yara4a/CityRate.git
cd CityRate
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Apply migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 4. Populate the database

```bash
python import_cities.py
python population_script.py
```

### 5. Run the server

```bash
python manage.py runserver
```

### 6. Open in browser

http://127.0.0.1:8000/

---

## 👤 How to Use

1. Create an account or log in  
2. Write a review for a city  
3. Save it as a draft or publish it  
4. Edit or delete your reviews from your account page  
5. Browse and search reviews from other users  

---

## 🧪 Testing

Run the test suite using:

```bash
python manage.py test
```

Tests cover:
- User authentication
- Review creation and validation
- Permissions (edit/delete)
- Core view functionality

---

## 📁 Project Structure

```
CityRate/
├── city/                  # Main Django app
├── templates/             # HTML templates
├── static/                # CSS, JS, images
├── population_script.py   # Generates sample data
├── import_cities.py       # Imports city dataset
├── requirements.txt
└── manage.py
```

---

## 📌 Notes

- The database file (`db.sqlite3`) is not included and will be generated after running migrations.
- The population script creates realistic sample data for demonstration.
- All JavaScript and CSS are stored in static files (no inline code).

---

## 🌐 Deployment

This project is designed to be deployable on PythonAnywhere.

---

## 👥 Team

- Sable  
- Yara  
- Abdullah  
- Rabindra  

---

## 📚 External Resources

- Bootstrap — https://getbootstrap.com/  
- Google Fonts — https://fonts.google.com/  
- Django Documentation — https://docs.djangoproject.com/  

---

## 📄 License

This project was developed for educational purposes.