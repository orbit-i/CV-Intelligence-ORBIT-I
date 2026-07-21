import re


def validate_required(value):
    return value.strip() != ""


def validate_email(email):
    pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
    return re.match(pattern, email) is not None


def validate_salary(salary):
    return salary.isdigit()