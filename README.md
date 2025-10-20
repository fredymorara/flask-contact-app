# Flask Contact Manager

A full-featured contact management web application built with Flask and MongoDB. It includes user authentication, a real-time WebSocket demo, and a clean, modern user interface.

---

## Features

- **Full User Authentication**:
  - User registration, login, and logout.
  - Secure password hashing using Werkzeug.
  - Session management with Flask-Login.
  - "Forgot Password" functionality with secure tokens and email delivery.
- **Complete Contact Management (CRUD)**:
  - **C**reate: Add new contacts with mobile, email, address, and registration number.
  - **R**ead: View all contacts in a clean, sortable dashboard.
  - **U**pdate: Edit existing contact details.
  - **D**elete: Remove contacts with a confirmation step.
- **Real-Time WebSocket Demo**:
  - A public chat room built with Flask-SocketIO to demonstrate real-time, bidirectional communication.
- **Modern UI**:
  - A polished and responsive user interface built with Bootstrap 5.
  - Icons from Bootstrap Icons for better visual navigation.
  - Clean card-based layouts and dismissible flash messages.
- **Project Documentation**:
  - Embedded documentation pages explaining the architecture and implementation of both the main app and the WebSocket demo.

---

## Getting Started

Follow these instructions to set up and run the project on your local machine.

### Prerequisites

- Python 3.8+
- A running MongoDB instance (local or on a service like MongoDB Atlas)

### 1. Clone the Repository

```bash
git clone https://github.com/fredymorara/flask-contact-app
cd flask-contact-app
```

### 2. Set Up a Virtual Environment

It is highly recommended to use a virtual environment to manage project dependencies.

```bash
# Create the virtual environment
python -m venv venv

# Activate it
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### 3. Install Dependencies

Install all required packages using the `requirements.txt` file.

```bash
pip install -r requirements.txt
pip install flask-socketio gunicorn eventlet
```

### 4. Configure Environment Variables

Create a `.env` file in the root of the project. This file will hold your secret keys and connection URIs. Copy the following into it and replace the placeholder values.

```
SECRET_KEY='a-long-random-secret-string-for-security'

# Your MongoDB connection string
MONGO_URI='mongodb://localhost:27017/contacts_db'

# Your Gmail credentials for sending password reset emails
# IMPORTANT: Use a Google App Password, not your regular password
MAIL_SERVER='smtp.gmail.com'
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME='your_email@gmail.com'
MAIL_PASSWORD='your-16-character-app-password'
```

### 5. Run the Application

Use the `run.py` script, which is configured to use the SocketIO server.

```bash
python run.py
```

The application will be available at `http://127.0.0.1:5000`.

---

## Project Structure

- `run.py`: Main entry point for the application.
- `config.py`: Handles configuration and environment variables.
- `app/`: The main application package.
  - `__init__.py`: Application factory, initializes Flask and extensions.
  - `models.py`: Data models and helpers for User and Contact.
  - `routes.py`: Defines all HTTP routes for the application.
  - `sockets.py`: Defines all server-side WebSocket event handlers.
  - `templates/`: Contains all Jinja2 HTML templates.
- `documentation/`: Contains documentation pages.

---

## Technologies Used

- **Backend**: Python, Flask, Flask-SocketIO, Gunicorn
- **Database**: MongoDB (with PyMongo)
- **Frontend**: HTML, CSS, Bootstrap 5
- **Authentication**: Flask-Login
- **Email**: Flask-Mail