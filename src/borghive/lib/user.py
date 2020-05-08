import random
import string


def generate_userid(uid_length):
    """generate random userid with ascii letters and digits"""
    letters = string.ascii_lowercase + string.digits
    return ''.join(random.choice(letters) for i in range(uid_length))
