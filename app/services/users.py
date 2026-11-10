from app.db import get_db_connection
import random


def generate_username(first_name, last_name):
    username_found = False
    created_username = first_name[0] + '.' + last_name

    while username_found == False:
        if username_exists(created_username):
            created_username = created_username + str(random.randint(0, 20))
            continue

        username_found = True

    return created_username


def username_exists(username):
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                select 1
                from users
                where username = %s
                """
                , (username,)
            )

            exists = cur.fetchone() is not None

    return exists


def email_exists(email):
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                select 1
                from users
                where email = %s
                """
                , (email,)
            )

            exists = cur.fetchone() is not None

    return exists