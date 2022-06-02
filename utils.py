"""
Set of small utilities for this project
"""


def convert_float(str_value):
    """"
    Converts given str to float
    """
    try:
        return float(str_value)
    except ValueError:
        return None

