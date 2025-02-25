# Flask Contact Management App

This is a Flask-based contact management application with user authentication, password reset functionality, and a MongoDB database.

## Description

This application allows users to:

* Register and log in.
* Add, search, and manage contacts.
* Request and reset passwords.

## Installation

1.  **Clone the repository:**

    ```bash
    git clone your_repository_url
    cd your_repository_directory
    ```

2.  **Create a virtual environment:**

    ```bash
    python -m venv venv
    venv\Scripts\activate  # On Windows
    source venv/bin/activate # On macOS/Linux
    ```

3.  **Install dependencies:**

    ```bash
    pip install -r requirements.txt
    ```
    * If you have not created a requirements.txt file, you can create one with the command `pip freeze > requirements.txt`

4.  **Create a `.env` file:**

    * Create a `.env` file in the root directory and add your environment variables:

    ```
    SECRET_KEY=your_secret_key
    MAIL_SERVER=smtp.gmail.com
    MAIL_PORT=587
    MAIL_USE_TLS=True
    MAIL_USERNAME=your_gmail_address@gmail.com
    MAIL_PASSWORD=your_app_password
    MONGO_URI=your_mongodb_uri
    ```

    * Replace the placeholder values with your actual data.

5.  **Run the application:**

    ```bash
    flask run
    ```

## Usage

1.  Open your browser and navigate to `http://127.0.0.1:5000`.
2.  Register a new user account or log in with existing credentials.
3.  Use the dashboard to add, search, and manage contacts.
4.  Use the password reset functionality if needed.

## Features

* User registration and login.
* Contact management (add, search).
* Password reset functionality.
* MongoDB database integration.
* Email sending via Flask-Mail.

## Technologies Used

* Python
* Flask
* Flask-Login
* Flask-Mail
* PyMongo
* MongoDB
* HTML/CSS

## Contributing

1.  Fork the repository.
2.  Create a new branch for your feature or bug fix.
3.  Commit your changes.
4.  Push to your branch.
5.  Submit a pull request.

## Contact

Fredrick M. Morara - momanyifredm@gmail.com - https://github.com/fredymorara