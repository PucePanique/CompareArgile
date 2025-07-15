from decimal import Decimal
from gettext import gettext as _

def validate_abc(a, b, c):
    try:
        a, b, c = Decimal(a), Decimal(b), Decimal(c)
    except ValueError:
        return False, _("A, B, and C must be decimal numbers.")

    total = a + b + c
    if not (99.5 <= total <= 100.5):
        return False, _("The sum of A, B, and C must be approximately 100 (±0.5).")

    return True, ""

def validate_legend(legend):
    return True, ""  # Accept all legends for now

def validate_color(color):
    if color == CONFIG['color_default']:
        return False, _("Please select a color.")
    return True, ""
