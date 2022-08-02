#!/usr/bin/env python
import random
import string


def token_gen(size=32, chars=string.ascii_uppercase + string.digits):
    """Generate uniq token"""
    return ''.join(random.choice(chars) for _ in range(size))
