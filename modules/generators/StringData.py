"""
==========
StringData
==========
"""

import random
import string

def random_string(random_length = None):
    """
    A generator for creating random string data of letters plus ' ' (whitespace)
    
    :params random_length: how many characters of random string data. if not provided, will be between 1 - 30
    :returns: String
    """
    choices = string.letters + ' '
    text = []
    if not random_length:
        random_length = random.randint(1, 30)
    for x in range(random_length):
        text.append(random.choice(choices))
    return "".join(text)