# 🧵 Social Media API (Django REST Framework)

A basic backend API for a social media application, built with Django and Django REST Framework (DRF).

## 🚀 Features

- JWT authentication (SimpleJWT)
- Create/view/delete posts
- Comment on posts
- Follow/unfollow users
- Feed showing posts from followed users

## 🛠️ Tech Stack

- Python 3
- Django
- Django REST Framework
- SimpleJWT

## ⚙️ Setup Instructions

1. Clone the repo:
   ```bash
   git clone https://github.com/yourusername/social-media-api-drf.git
   cd social-media-api-drf
   
2. Create virtual environment and activate:
    python -m venv env
    source env/bin/activate  # or env\Scripts\activate on Windows

3. Install dependencies:
   pip install -r requirements.txt

4. Run migrations:
   python manage.py migrate

5. Start the server:
   python manage.py runserver

6. Access API at http://127.0.0.1:8000/

📌 Notes

Uses JWT for login/logout

API-only project, no frontend (can be connected to React, etc.)