# 📝 Notes API

A **Django REST Framework (DRF)** powered API for managing notes with **JWT authentication**, **user profiles**, **follow system**, **comments/likes**, **pagination**, **filtering**, **throttling**, and **Algolia search**.

---

## 🚀 Features

- 🔑 **JWT Authentication** – secure login & token refresh
- 👤 **User Profiles** – bio, location, birth date, avatar
- 📝 **Notes** – create, update, delete, and list your notes
- 💬 **Comments** – add comments and like/unlike them
- ❤️ **Likes** – like/unlike notes and comments (toggle system)
- 🔗 **Follow/Unfollow** – follow users and get personalized feeds
- 🔍 **Search** – Algolia-powered full-text search across notes & profiles
- 📄 **Pagination & Filtering** – query notes with filters
- ⚡ **Throttling** – rate limiting for API safety
- 🛡 **Permissions** – users only access their own notes & profiles

---

## ⚙️ Installation

1. **Clone the repo**

```bash
git clone https://github.com/Daniel7303/notes-api.git
cd notes-api
```

2. **Create & activate virtual environment**

```bash
python -m venv venv
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate
```

3. **Install dependencies**

```bash
pip install -r requirements.txt
```

4. **Environment variables**

Create a `.env` file in the project root:

```env
SECRET_KEY=your_secret_key
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost

# JWT
ACCESS_TOKEN_LIFETIME=3600
REFRESH_TOKEN_LIFETIME=86400

# Algolia
ALGOLIA_APP_ID=your_app_id
ALGOLIA_API_KEY=your_admin_api_key
ALGOLIA_SEARCH_KEY=your_search_only_api_key
```

⚠️ Don’t commit `.env` to Git (already in `.gitignore`).

5. **Run migrations**

```bash
python manage.py makemigrations
python manage.py migrate
```

6. **Create superuser (optional)**

```bash
python manage.py createsuperuser
```

7. **Run server**

```bash
python manage.py runserver
```

---

## 🗂 Project Structure

```
Note_api/
│── accounts/         # Handles user profiles, auth, followers
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   ├── urls.py
│
│── api/              # Handles notes, comments, likes
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   ├── urls.py
│
│── Note_api/         # Project settings
│   ├── settings.py
│   ├── urls.py
│
│── manage.py
│── requirements.txt
│── README.md
│── .env
```

---

## 🔑 Authentication

This project uses **JWT Authentication (SimpleJWT)**.

**Obtain tokens:**

```http
POST /api/token/
{
  "username": "yourusername",
  "password": "yourpassword"
}
```

**Response:**

```json
{
  "refresh": "your_refresh_token",
  "access": "your_access_token"
}
```

**Use access token in headers:**

```
Authorization: Bearer your_access_token
```

---

## 📌 API Endpoints

### 🔹 Auth

- `POST /api/token/` → Get JWT tokens
- `POST /api/token/refresh/` → Refresh access token

### 🔹 Profile

- `GET /api/profile/` → Get logged-in user’s profile
- `PATCH /api/profile/` → Update your profile

### 🔹 Notes

- `GET /api/notes/` → List your notes
- `POST /api/notes/` → Create new note
- `GET /api/notes/{id}/` → Retrieve single note
- `PATCH /api/notes/{id}/` → Update your note
- `DELETE /api/notes/{id}/` → Delete your note

### 🔹 Comments & Likes

- `POST /api/notes/{id}/comment/` → Add comment
- `POST /api/comment/{id}/like/` → Like/unlike a comment
- `POST /api/notes/{id}/like/` → Like/unlike a note

### 🔹 Followers

- `POST /api/follow/{user_id}/` → Follow user
- `DELETE /api/follow/{user_id}/` → Unfollow user
- `GET /api/feed/` → Get notes from followed users

### 🔹 Search

- `GET /api/search/?q=keyword` → Search notes & profiles

---

## 📷 Example Response (Profile)

```json
{
  "user": "daniel",
  "bio": "Backend dev learning DRF",
  "location": "Nigeria",
  "birth_date": "1998-04-21",
  "avatar": "http://127.0.0.1:8000/media/avatars/daniel.png"
}
```

---

## 🛠 Tech Stack

- Python 3.12+
- Django 5.2.5
- Django REST Framework
- SimpleJWT (JWT authentication)
- Algolia (search)
- SQLite (default DB, can switch to Postgres in production)

---
