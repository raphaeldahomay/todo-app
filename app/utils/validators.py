import re

def is_valid_password(password):
    return (
        len(password) >= 8
        and any(char.isdigit() for char in password)
        and bool(re.search(r"[^a-zA-Z0-9]", password))
    )