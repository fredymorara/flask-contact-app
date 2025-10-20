from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from flask_mail import Message
from app import app, db, mail
from app.models import User, Contact
from werkzeug.security import generate_password_hash
import secrets
from datetime import datetime, timedelta  # Import timedelta
from bson import ObjectId # Import ObjectId


@app.route('/')
@app.route('/index')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        remember = request.form.get('remember', False)

        if not username or not password:
            flash('Please fill in all fields.', 'danger')
            return redirect(url_for('login'))

        user = User.get_by_username(username)

        if user and user.check_password(password):
            login_user(user, remember=remember)
            next_page = request.args.get('next')
            if next_page:
                return redirect(next_page)
            flash('Login successful!', 'success')
            return redirect(url_for('dashboard'))

        flash('Invalid username or password', 'danger')

    return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')

        if not username or not email or not password:
            flash('Please fill in all fields.', 'danger')
            return redirect(url_for('register'))

        existing_user = User.get_by_username(username)
        if existing_user:
            flash('Username already exists.', 'danger')
            return redirect(url_for('register'))

        existing_email = User.get_by_email(email)
        if existing_email:
            flash('Email already exists.', 'danger')
            return redirect(url_for('register'))

        new_user = User(username=username, email=email)
        new_user.set_password(password)
        hashed_password = generate_password_hash(password)
        db.users.insert_one({
            'username': username,
            'email': email,
            'password_hash': hashed_password
        })

        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('login'))

    return render_template('register.html')


@app.route('/reset_password_request', methods=['GET', 'POST'])
def reset_password_request():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    if request.method == 'POST':
        email = request.form.get('email')

        if not email:
            flash('Please enter your email address.', 'danger')
            return redirect(url_for('reset_password_request'))

        user = User.get_by_email(email)

        if user:
            token = secrets.token_urlsafe(32)
            # Store the reset token in MongoDB with expiration
            db.password_resets.insert_one({
                'user_id': user._id,
                'token': token,
                'timestamp': datetime.utcnow()
            })

            # Send reset email
            reset_url = url_for('reset_password', token=token, _external=True)
            msg = Message('Password Reset Request',
                          sender=app.config['MAIL_USERNAME'],
                          recipients=[user.email])
            msg.body = f'''To reset your password, visit the following link:
{reset_url}

This link will expire in 24 hours.
If you did not make this request, please ignore this email.
'''
            mail.send(msg)

        # Always show this message even if email doesn't exist (security best practice)
        flash('If your email is registered, you will receive password reset instructions. Check Spam folder if you cant see it', 'info')
        return redirect(url_for('login'))

    return render_template('reset_password_request.html')


@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    # Find the reset token in the database
    reset_data = db.password_resets.find_one({
        'token': token,
        'timestamp': {'$gte': datetime.utcnow() - timedelta(days=1)}  # Token valid for 24 hours
    })

    if not reset_data:
        flash('Invalid or expired reset link.', 'danger')
        return redirect(url_for('login'))

    if request.method == 'POST':
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')

        if not password or not confirm_password:
            flash('Please fill in all fields.', 'danger')
            return redirect(url_for('reset_password', token=token))

        if password != confirm_password:
            flash('Passwords do not match.', 'danger')
            return redirect(url_for('reset_password', token=token))

        # Use User.get_by_id instead of load_user
        user = User.get_by_id(str(reset_data['user_id']))
        
        if user:
            user.set_password(password)
            db.users.update_one(
                {'_id': ObjectId(user._id)},
                {'$set': {'password_hash': user.password_hash}}
            )
            # Delete the used token
            db.password_resets.delete_one({'token': token})
            flash('Your password has been reset successfully.', 'success')
            return redirect(url_for('login'))
        else:
            flash('User not found.', 'danger')
            return redirect(url_for('login'))

    return render_template('reset_password.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('login'))


@app.route('/dashboard')
@login_required
def dashboard():
    contacts = list(db.contacts.find({'user_id': current_user._id}))
    return render_template('dashboard.html', contacts=contacts)


@app.route('/contact_form', methods=['GET', 'POST'])
@login_required
def contact_form():
    if request.method == 'POST':
        mobile = request.form.get('mobile')
        email = request.form.get('email')
        address = request.form.get('address')
        reg_number = request.form.get('reg_number')

        if not mobile or not email or not address or not reg_number:
            flash('Please fill in all fields.', 'danger')
            return redirect(url_for('contact_form'))

        existing_contact = Contact.get_by_reg_number(reg_number)
        if existing_contact:
            flash('Contact with this registration number already exists.', 'danger')
            return redirect(url_for('contact_form'))

        contact = Contact(mobile=mobile, email=email, address=address, reg_number=reg_number, user_id=current_user._id)
        contact.save()
        flash('Contact added successfully!', 'success')
        return redirect(url_for('dashboard'))

    return render_template('contact_form.html')


@app.route('/search', methods=['GET', 'POST'])
@login_required
def search():
    if request.method == 'POST':
        search_term = request.form.get('search_term')
        search_results = list(db.contacts.find({
            'user_id': current_user._id,
            '$or': [
                {'mobile': {'$regex': search_term, '$options': 'i'}},
                {'email': {'$regex': search_term, '$options': 'i'}},
                {'address': {'$regex': search_term, '$options': 'i'}},
                {'reg_number': {'$regex': search_term, '$options': 'i'}}
            ]
        }))
        return render_template('search.html', results=search_results, search_term=search_term)
    return render_template('search.html')

@app.route('/edit_contact/<contact_id>', methods=['GET', 'POST'])
@login_required
def edit_contact(contact_id):
    # Find the specific contact, ensuring it belongs to the logged-in user
    contact = db.contacts.find_one({'_id': ObjectId(contact_id), 'user_id': current_user._id})

    if not contact:
        flash('Contact not found or you do not have permission.', 'danger')
        return redirect(url_for('dashboard'))

    if request.method == 'POST':
        # Get updated data from the form
        mobile = request.form.get('mobile')
        email = request.form.get('email')
        address = request.form.get('address')
        reg_number = request.form.get('reg_number')

        # Run validation
        if not mobile or not email or not address or not reg_number:
            flash('Please fill in all fields.', 'danger')
            # Pass contact back to template to re-fill the form
            return render_template('edit_contact.html', contact=contact)

        # Update the contact in MongoDB
        db.contacts.update_one(
            {'_id': ObjectId(contact_id)},
            {'$set': {
                'mobile': mobile,
                'email': email,
                'address': address,
                'reg_number': reg_number
            }}
        )
        flash('Contact updated successfully!', 'success')
        return redirect(url_for('dashboard'))

    # On a GET request, show the form pre-filled with the contact's data
    return render_template('edit_contact.html', contact=contact)

@app.route('/delete_contact/<contact_id>')
@login_required
def delete_contact(contact_id):
    # Try to delete the contact, ensuring it belongs to the current user
    result = db.contacts.delete_one({'_id': ObjectId(contact_id), 'user_id': current_user._id})

    if result.deleted_count > 0:
        flash('Contact deleted successfully.', 'success')
    else:
        # This can happen if the contact doesn't exist or doesn't belong to the user
        flash('Error: Could not delete contact.', 'danger')
        
    return redirect(url_for('dashboard'))

@app.route('/websocket_demo')
def websocket_demo():
    # This route is public, no @login_required
    return render_template('websocket_demo.html')

@app.route('/documentation/contact-app')
def docs_contact_app():
    """Serves the documentation page for the main Flask app."""
    return render_template('docs_contact_app.html')

@app.route('/documentation/websocket')
def docs_websocket():
    """Serves the documentation page for the WebSocket demo."""
    return render_template('docs_websocket.html')

@app.route('/test_email')
def test_email():
    msg = Message('Test Email', sender=app.config['MAIL_USERNAME'], recipients=['capsboost@gmail.com'])  # Replace with your email
    msg.body = 'This is a test email from your Flask app.'
    mail.send(msg)
    return 'Test email sent!'