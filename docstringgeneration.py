"""
    Generates a random number between the specified start and end values.

    Parameters:
    start (int): The lower bound of the range (inclusive).
    end (int): The upper bound of the range (inclusive).

    Returns:
    int: A random number between start and end.
    """

import random
def generate_number(start, end):

    return random.randint(start, end)