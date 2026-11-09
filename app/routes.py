from flask import Blueprint, render_template, session, url_for, request, redirect
from werkzeug.security import check_password_hash, generate_password_hash
from app.db import get_db_connection
from app.utils.validators import is_valid_password
from app.services.users import generate_username



main = Blueprint("main", __name__)



@main.route('/')
def main_page():
    return render_template('index.html')



@main.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')

    email_or_username = request.form.get('email_username')
    password = request.form.get('password')

    if not email_or_username or not password:
        return render_template('login.html', error='All fields are required.'), 400

    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT
                    user_id
                    , pwd_hash
                FROM users
                WHERE email = %s
                   OR username = %s
                """,
                (email_or_username, email_or_username)
            )

            user = cur.fetchone()

    if user is None or not check_password_hash(user[1], password):
        return render_template('login.html', error='Invalid credentials.'), 401

    session.clear()
    session['user_id'] = str(user[0])

    return redirect(url_for('main.main_page'))



@main.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'GET':
        return render_template('signup.html')

    first_name = request.form.get('first_name')
    last_name = request.form.get('last_name')
    email = request.form.get('email')
    password = request.form.get('password')

    if not is_valid_password(password):
        return render_template(
            'signup.html',
            error='Password must contain at least 8 characters, 1 digit, and 1 special character.'
        ), 400

    password_hash = generate_password_hash(password)

    if not first_name or not last_name or not email or not password_hash:
        return render_template('signup.html', error='All fields are required.'), 400

    username = generate_username(first_name, last_name)

    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                update table users
                set
                    first_name = %s
                    , last_name = %s
                    , email = %s
                    , username = %s
                    , pwd_hash = %s
                """,
                (first_name, last_name, email, username, password_hash)
            )

            user = cur.fetchone()

    


@main.rounte('/create_folder')
def create_folder():
    is_authenticated = bool(session.get("user_id"))

    if is_authenticated:
        return 
    
    return redirect(url_for('main.login'))