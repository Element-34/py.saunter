import random
import string

def random_string(random_length = None):
    choices = string.letters + ' '
    text = []
    if not random_length:
        random_length = random.randint(1, 30)
    for x in range(random_length):
        text.append(random.choice(choices))
    return "".join(text)