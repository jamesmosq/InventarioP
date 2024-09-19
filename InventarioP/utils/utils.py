# utils/utils.py

def validate_float(value):
    try:
        return float(value)
    except ValueError:
        return None

def validate_int(value):
    try:
        return int(value)
    except ValueError:
        return None

def format_currency(value):
    return f"${value:.2f}"