# helper.py
"""
This module provides general helper functions and classes.
"""

import random
import string
from datetime import datetime

TIMESTAMP_WITH_TIMEZONE_FORMAT = '%Y-%m-%dT%H:%M:%S.%f%z'


class GeneralObject:
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)


def get_utc_now():
    return datetime.utcnow()


def generate_random_string(length=8):
    """Generate a random string of fixed length."""
    letters = string.ascii_letters + string.digits
    return ''.join(random.choice(letters) for i in range(length))
