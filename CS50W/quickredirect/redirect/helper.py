import random
import string

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