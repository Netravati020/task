# 🧾 User Activity Log API

This project is a Django REST Framework (DRF) based backend system to track user activities like login, logout, file uploads, etc., with robust API design, authentication, Redis caching, status workflows, and complete unit testing.

---

## 🚀 Features

- User activity logging (LOGIN, LOGOUT, UPLOAD_FILE, etc.)
- RESTful API to POST, GET, and PATCH logs
- Filtering by action and date range
- Workflow status transitions (`PENDING`, `IN_PROGRESS`, `DONE`)
- Redis caching (1-minute cache for GET queries)
- Token authentication
- Admin panel support
- Unit tests and optional Swagger documentation

---

## Installations

python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py drf_create_token your_username

python manage.py test activity
http://127.0.0.1:8000/api/activity/logs/
