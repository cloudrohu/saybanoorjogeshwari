# utility/context_processors.py
from home.models import Setting
# Note: Agar aapne Home app ke models ko 'home' se import karne mein dikkat aati hai,
# toh 'realestate_portal.home.models' bhi use kar sakte hain.

def global_settings_processor(request):
    """
    Context processor to make site-wide settings available in all templates.
    """
    try:
        # Fetch the main site settings object
        settings = Setting.objects.first()
    except Exception:
        settings = None

    # Return a dictionary. Its keys become context variables available in all templates.
    return {
        'site_settings': settings,
        # Agar aapko Top-Level MPTT Types chahiye (e.g., Residential/Commercial)
        # unko bhi yahan se fetch kiya ja sakta hai
    }