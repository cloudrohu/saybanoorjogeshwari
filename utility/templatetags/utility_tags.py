# utility/templatetags/utility_tags.py
from django import template
from decimal import Decimal

register = template.Library()

@register.filter(name='in_unit')
def indian_unit_format(value):
    """
    Formats an integer price into Lakhs (L) or Crores (Cr) units.
    Example: 50000000 -> 5.0 Cr | 4750000 -> 47.5 L
    """
    if value is None or value == "":
        return ""
        
    try:
        # Decimal type mein convert karein for accurate float math
        amount = Decimal(value)
    except:
        return value # If conversion fails, return original value
        
    # 1 Crore = 10,000,000
    CR_UNIT = Decimal('10000000')
    # 1 Lakh = 100,000
    LAKH_UNIT = Decimal('100000')
    
    # --- 1. Crore Formatting ---
    if amount >= CR_UNIT:
        # Crores mein divide karein aur 2 decimal places tak round off karein
        crore_value = amount / CR_UNIT
        # Example: 50000000 / 10000000 = 5.0
        # Example: 12345678 / 10000000 = 1.23
        return f'{crore_value:.2f} Cr' 

    # --- 2. Lakh Formatting ---
    elif amount >= LAKH_UNIT:
        # Lakhs mein divide karein aur 2 decimal places tak round off karein
        lakh_value = amount / LAKH_UNIT
        # Example: 4750000 / 100000 = 47.50
        return f'{lakh_value:.2f} L'
        
    # --- 3. Less than 1 Lakh (Return as normal) ---
    else:
        # Agar ₹1 lakh se kam hai, toh sirf comma format use karein (optional, can return as is)
        return str(amount)