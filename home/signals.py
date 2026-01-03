from django.db.models.signals import post_save
from django.dispatch import receiver
from PIL import Image
import os
from .models import (
    Setting, Slider, Leadership, Why_Choose, About,
    Contact_Page, Our_Team, Testimonial
)

# =============================
# ⚙️ Configuration
# =============================
THUMBNAIL_SIZE = (300, 300)
MAX_SIZE_MB = 2


# =============================
# ⚙️ Helper Functions
# =============================

def get_file_size_mb(path):
    """Return file size in MB"""
    return os.path.getsize(path) / (1024 * 1024)


def compress_and_thumbnail(image_path):
    """Compress image + generate thumbnail (WebP)"""
    if not image_path or not os.path.exists(image_path):
        return None, None

    img = Image.open(image_path)
    img = img.convert("RGB")

    # Resize if > 2MB
    if get_file_size_mb(image_path) > MAX_SIZE_MB:
        img.thumbnail((1600, 1600))

    # Save compressed WebP
    webp_path = image_path.rsplit(".", 1)[0] + ".webp"
    img.save(webp_path, format="WEBP", quality=75)

    # Thumbnail
    thumb_img = img.copy()
    thumb_img.thumbnail(THUMBNAIL_SIZE)
    thumb_path = image_path.rsplit(".", 1)[0] + "_thumb.webp"
    thumb_img.save(thumb_path, format="WEBP", quality=80)

    # Delete original
    try:
        os.remove(image_path)
    except Exception:
        pass

    return webp_path, thumb_path


def process_image_field(instance, field_name):
    """Compress and replace any model image field"""
    image_field = getattr(instance, field_name, None)
    if not image_field or not image_field.name:
        return

    # Skip already compressed files
    if str(image_field.name).endswith(".webp"):
        return

    try:
        webp_path, thumb_path = compress_and_thumbnail(image_field.path)
        if webp_path:
            relative_webp_path = image_field.name.rsplit(".", 1)[0] + ".webp"
            setattr(instance, field_name, relative_webp_path)
            instance.save(update_fields=[field_name])
    except Exception as e:
        print(f"⚠️ Image compression failed for {field_name}: {e}")


# =============================
# 🔔 Signal Handlers
# =============================

# ✅ Settings Model
@receiver(post_save, sender=Setting)
def compress_setting_images(sender, instance, **kwargs):
    for field in ["logo", "favicon", "search_bg", "testmonial_bg"]:
        process_image_field(instance, field)


# ✅ Slider Model
@receiver(post_save, sender=Slider)
def compress_slider_image(sender, instance, **kwargs):
    process_image_field(instance, "image")


# ✅ Leadership Model
@receiver(post_save, sender=Leadership)
def compress_leadership_image(sender, instance, **kwargs):
    process_image_field(instance, "image")


# ✅ Why Choose Model
# (No image field in this model — skipping intentionally)


# ✅ About Model
@receiver(post_save, sender=About)
def compress_about_images(sender, instance, **kwargs):
    for field in ["image", "search_bg", "home_bg"]:
        process_image_field(instance, field)


# ✅ Contact Page
@receiver(post_save, sender=Contact_Page)
def compress_contact_image(sender, instance, **kwargs):
    # This model has no image field — kept for consistency
    pass


# ✅ Our Team
@receiver(post_save, sender=Our_Team)
def compress_team_image(sender, instance, **kwargs):
    process_image_field(instance, "image")


# ✅ Testimonial
@receiver(post_save, sender=Testimonial)
def compress_testimonial_image(sender, instance, **kwargs):
    process_image_field(instance, "image")
