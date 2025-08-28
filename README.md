# notes-api

A Django REST API for managing notes with JWT authentication, user profiles, following system, pagination, filtering, and throttling.

📒 Note API (DRF Project)

A simple Note-Taking API built with Django REST Framework (DRF).
It includes user authentication, profiles, notes, and follower relationships.

🚀 Features

User registration & login with JWT authentication.

User profiles (bio, location, birth date, avatar).

Users can create, update, delete, and view their own notes.

Users can follow/unfollow others and view their followers.

Protected routes: users only access their own data.

⚙️ Installation

1. Clone the repo
   git clone https://github.com/Daniel7303/notes-api.git
   cd note-api

2. Create and activate virtual environment
   python -m venv venv

# Windows

venv\Scripts\activate

# Linux/Mac

source venv/bin/activate

3. Install dependencies
   pip install -r requirements.txt

4. Run migrations
   python manage.py makemigrations
   python manage.py migrate

5. Create superuser (optional, for admin access)
   python manage.py createsuperuser

6. Run server
   python manage.py runserver

🗂 Project Structure
Note_api/
│── accounts/ # Handles user profiles, auth, followers
│ ├── models.py
│ ├── serializers.py
│ ├── views.py
│ ├── urls.py
│
│── notes/ # Handles user notes
│ ├── models.py
│ ├── serializers.py
│ ├── views.py
│ ├── urls.py
│
│── Note_api/ # Project settings
│ ├── settings.py
│ ├── urls.py
│
│── manage.py
│── requirements.txt
│── README.md

🔑 Authentication

This project uses JWT Authentication.

Obtain tokens:

POST /api/token/
{
"username": "yourusername",
"password": "yourpassword"
}

Response:

{
"refresh": "your_refresh_token",
"access": "your_access_token"
}

Use access token in headers:

Authorization: Bearer your_access_token

📌 API Endpoints
🔹 Auth

POST /api/token/ → Get JWT tokens

POST /api/token/refresh/ → Refresh access token

🔹 Profile

GET /api/profile/ → Get logged-in user’s profile

PATCH /api/profile/ → Update your profile

🔹 Notes

GET /api/notes/ → List your notes

POST /api/notes/ → Create new note

GET /api/notes/{id}/ → Retrieve single note

PATCH /api/notes/{id}/ → Update your note

DELETE /api/notes/{id}/ → Delete your note

🔹 Followers

GET /api/followers/ → List followers

(upcoming) POST /api/follow/{user_id}/ → Follow a user

(upcoming) DELETE /api/unfollow/{user_id}/ → Unfollow a user

📷 Example Response (Profile)
{
"user": "daniel",
"bio": "Backend dev learning DRF",
"location": "Nigeria",
"birth_date": "1998-04-21",
"avatar": "http://127.0.0.1:8000/media/avatars/daniel.png"
}

🛠 Tech Stack

Python 3.12+

Django 5.2.5

Django REST Framework

Simple JWT

SQLite (default DB)
