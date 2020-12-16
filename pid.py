import hashlib
import random
import string

def random_pid():
    pid_val=hashlib.sha256(__random_string(10).encode('ascii')).hexdigest()
    return f'PID:{pid_val}'

def __random_string(size=10):
    # Random string with the combination of lower and upper case
    letters = string.ascii_letters
    result_str = ''.join(random.choice(letters) for i in range(size))
    return result_str
