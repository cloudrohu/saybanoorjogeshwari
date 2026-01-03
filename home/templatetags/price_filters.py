from django import template
register = template.Library()

@register.filter
def indian_price(value):
    try:
        value = int(value)
    except:
        return ""

    if value >= 10000000:
        return f"{value/10000000:.2f} Cr"
    elif value >= 100000:
        return f"{value/100000:.0f} L"
    return f"{value:,}"
