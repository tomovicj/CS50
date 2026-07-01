import random
import string
import re


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def generate_id():
    characters = string.ascii_lowercase + string.digits
    id = ''.join(random.choice(characters) for i in range(6))
    return id


def is_valid_id(id):
    pattern = r'^(?=.{3,15}$)[a-zA-Z0-9]+$'
    if re.fullmatch(pattern, id):
        return True
    return False


def is_valid_email(email):
    email_pattern = r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+'
    if re.fullmatch(email_pattern, email):
        return True
    return False
