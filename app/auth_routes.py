from flask import Blueprint, render_template, session, url_for, request, redirect
from werkzeug.security import check_password_hash, generate_password_hash
from app.db import get_db_connection
from app.utils.validators import is_valid_password
from app.services.users import generate_username, email_exists
from psycopg.errors import UniqueViolation, UndefinedTable
from psycopg import OperationalError



main = Blueprint("main", __name__)



@main.route('/')
def main_page():
    user_id = session.get('user_id')
    folder_id = request.args.get('folder_id')

    folders = []
    selected_folder = None
    tasks = []

    if user_id:
        with get_db_connection() as conn:
            with conn.cursor() as cur:

                # Retrieve all user folders
                cur.execute(
                    """
                    select
                        folder_id
                        , folder_name
                        , created_at
                    from folders
                    where user_id = %s
                        and is_deleted = FALSE
                    order by created_at desc
                    """,
                    (user_id,)
                )

                folders = cur.fetchall()

                # Retrieve selected folder and its tasks
                if folder_id:
                    cur.execute(
                        """
                        select
                            folder_id
                            , folder_name
                            , created_at
                        from folders
                        where folder_id = %s
                            and user_id = %s
                            and is_deleted = FALSE
                        """,
                        (folder_id, user_id)
                    )

                    selected_folder = cur.fetchone()

                    if selected_folder:
                        cur.execute(
                            """
                            select
                                task_id
                                , task_desc
                                , is_done
                            from tasks
                            where folder_id = %s
                                and is_deleted = FALSE
                            order by created_at desc
                            """,
                            (folder_id,)
                        )

                        tasks = cur.fetchall()

    return render_template(
        'index.html',
        folders=folders,
        selected_folder=selected_folder,
        tasks=tasks
    )


@main.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')

    email_or_username = request.form.get('email_username')
    password = request.form.get('password')

    if not email_or_username or not password:
        return render_template('login.html', error='All fields are required.'), 400

    try:
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

    except OperationalError:
        return render_template(
            'login.html',
            error='Database connection failed. Please try again later.'
        ), 503

    except UndefinedTable:
        return render_template(
            'login.html',
            error='These credentials do not exist.'
        ), 503
    
    except Exception:
        raise 

    if user is None or not check_password_hash(user[1], password):
        return render_template('login.html', error='Invalid credentials.'), 401

    session.clear()
    session['user_id'] = str(user[0])

    return redirect(url_for('main.main_page'))



@main.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'GET':
        return render_template('signup.html')

    first_name = (request.form.get('first_name') or '').strip()
    last_name = (request.form.get('last_name') or '').strip()
    email = (request.form.get('email') or '').strip().lower()
    password = request.form.get('password')

    if not all([first_name, last_name, email, password]):
        return render_template('signup.html', error='All fields are required.'), 400

    if not is_valid_password(password):
        return render_template(
            'signup.html',
            error='Password must contain at least 8 characters, 1 digit, and 1 special character.'
        ), 400

    if email_exists(email):
        return render_template('signup.html', error='This email already exists.'), 400

    password_hash = generate_password_hash(password)
    username = generate_username(first_name, last_name)

    try:
        with get_db_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    INSERT INTO users (
                        first_name,
                        last_name,
                        email,
                        username,
                        pwd_hash
                    )
                    VALUES (%s, %s, %s, %s, %s)
                    RETURNING user_id
                    """,
                    (
                        first_name,
                        last_name,
                        email,
                        username,
                        password_hash
                    )
                )

                user_id = cur.fetchone()[0]

    except UniqueViolation:
        return render_template('signup.html', error='Email or username already exists.'), 409

    except OperationalError:
        return render_template(
            'signup.html',
            error='Database connection failed. Please try again later.'
        ), 503

    except Exception:
        raise

    if user_id is None:
        return render_template('signup.html', error='An error occurred, try again later.'), 400

    return redirect(url_for('main.login'))



@main.route('/logout', methods=['GET', 'POST'])
def logout():
    if not session.get('user_id'):
        return render_template('index.html', error='You are already logged out.'), 400

    session.clear()

    return redirect(url_for('main.main_page'))
