from app import app
from flask import render_template, redirect, url_for, session, request
from flask import flash, jsonify
from .models import db, User
from datetime import datetime


@app.route('/')
def index():
    if 'username' in session:
        return redirect(url_for('main'))
    return render_template('index.html')


@app.route('/signup')
def signup():
    if 'username' in session:
        return redirect(url_for('main'))
    return render_template('signup.html')


@app.route('/signup', methods=['POST'])
def handle_signup():
    if request.method == 'POST':
        username = request.form['username']
        fullname = request.form['fullname']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confpassword']

        # Check if username is already used
        if User.query.filter_by(Username=username).first():
            flash('Username already in use. Please choose another.', 'error')
            return redirect(url_for('signup'))

        # Check if email is already used
        if User.query.filter_by(Email=email).first():
            flash('Email already in use. Please use another email.', 'error')
            return redirect(url_for('signup'))

        # Check if password and its confirmation match
        if password != confirm_password:
            flash('Password and confirmation do not match. Please try again.', 'error')
            return redirect(url_for('signup'))

        new_user = User(
                Username=username,
                FullName=fullname,
                Email=email,
                Password=password
                )

        db.session.add(new_user)
        db.session.commit()

        flash('Registration successful. You can now log in!', 'success')
        return redirect(url_for('signup'))

    return render_template('signup.html')


@app.route('/login')
def login():
    if 'username' in session:
        return redirect(url_for('main'))
    return render_template('login.html')


@app.route('/login', methods=['POST'])
def handle_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if not User.query.filter_by(Username=username).first():
            flash('Invalid username.', 'error')
        else:
            if not User.query.filter_by(Username=username, Password=password).first():
                flash('Password incorrect.', 'error')
            else:
                user = User.query.filter_by(Username=username, Password=password).first()
                session['user_id'] = user.UserID
                session['username'] = user.Username
                session['fullname'] = user.FullName
                session['email'] = user.Email
                return redirect(url_for('main'))
        return redirect(url_for('login'))


@app.route('/main')
def main():
    if 'user_id' not in session:
        return redirect(url_for('index'))
    return render_template('main.html')


@app.route('/search')
def search_results():
    if 'user_id' not in session:
        return redirect(url_for('index'))
    query = request.args.get('query', '')
    if len(query) != 0:
        return render_template('search.html', query=query)
    return render_template('search.html')


@app.route('/logout')
def logout():
    try:
        # Check if the user is logged in
        if 'user_id' in session:
            # Get the user ID
            user_id = session['user_id']

            # Update the Last_Active attribute in the User table
            user = User.query.filter_by(UserID=user_id).first()
            user.Last_Active = datetime.now()

            # Commit the changes to the database
            db.session.commit()

            # Clear session data
            session.clear()

        return redirect(url_for('index'))

    except Exception as e:
        return jsonify({'error': str(e)}), 500

