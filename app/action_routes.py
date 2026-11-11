from flask import render_template, session, url_for, request, redirect
from app.db import get_db_connection
from psycopg import OperationalError
from app.auth_routes import main



@main.route('/create_folder', methods=['GET', 'POST'])
def create_folder():
    user_id = session.get("user_id")
    is_authenticated = bool(user_id)

    if is_authenticated:
        folder_name = (request.form.get('folder_name') or '').strip().lower()

        if not folder_name:
            return render_template('index.html', error='Please enter a valid folder name.'), 400

        try:
            with get_db_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute(
                        """
                        insert into folders(
                            user_id
                            , folder_name
                        )
                        values(%s, %s)
                        returning folder_id
                        """,
                        (user_id, folder_name)
                    )

                    folder_id = cur.fetchone()[0]

        except OperationalError:
            return render_template('index.html', error='Sorry an error occurred. Try again later'), 400

        if folder_id is None:
            return render_template('index.html', error='Sorry an error occurred. Try again later'), 400
    
        return redirect(url_for('main.main_page'))

    return redirect(url_for('main.login'))



@main.route('/delete-folder', methods=['GET', 'POST'])
def delete_folder():
    user_id = session.get("user_id")
    is_authenticated = bool(user_id)

    if not is_authenticated:
        return render_template('login.html', error='Please logged-in first.')

    folder_id = request.get_json()['folder_id']

    try:
        with get_db_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    update folders
                    set
                        is_deleted = true
                        , updated_at = current_timestamp
                    where folder_id = %s
                        and user_id = %s
                    """
                    , (folder_id, user_id,)
                )

    except OperationalError:
        return render_template('index.html', error='Sorry an error occurred. Try again later'), 400

    return {'success': True}, 200 



@main.route('/create_task', methods=['GET', 'POST'])
def create_task():
    user_id = session.get('user_id')

    folder_id = request.form.get('folder_id')
    task_desc = request.form.get('task_desc')

    if user_id is None:
        return redirect(url_for('login'))

    try:
        with get_db_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    insert into tasks(
                        folder_id
                        , task_desc  
                    )
                    values(%s, %s)
                    """,
                    (folder_id, task_desc)
                )

    except OperationalError:
        return render_template('index.html', error='Sorry an error occurred. Try again later'), 400
    
    return redirect(url_for('main.main_page', folder_id=folder_id))



@main.route('/toggle-task', methods=['POST'])
def toggle_task():
    data = request.get_json()

    task_id = data.get('task_id')
    is_done = data.get('is_done')

    try:
        with get_db_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    update tasks
                    set
                        is_done = %s
                        , updated_at = current_timestamp
                    where task_id = %s
                    """,
                    (is_done, task_id)
                )

    except OperationalError:
        return render_template('index.html', error='Sorry an error occurred. Try again later'), 400

    return {'success': True}, 200



@main.route('/delete-task', methods=['GET', 'POST'])
def delete_task():
    user_id = session.get("user_id")
    is_authenticated = bool(user_id)

    if not is_authenticated:
        return render_template('login.html', error='Please logged-in first.')

    task_id = request.get_json()['task_id']

    try:
        with get_db_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    update tasks
                    set
                        is_deleted = true
                        , updated_at = current_timestamp
                    where task_id = %s
                    """
                    , (task_id,)
                )

    except OperationalError:
        return render_template('index.html', error='Sorry an error occurred. Try again later'), 400

    return {'success': True}, 200 