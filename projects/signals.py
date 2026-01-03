# project/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from PIL import Image
import os


from .models import (
    Project, Gallery,Header,WebSlider,RERA_Info
)



def process_image_field(instance, field_name):
    image_field = getattr(instance, field_name)
    if image_field and not str(image_field).endswith('.webp'):
        image_path = image_field.path

        # 1️⃣ Open image & convert to WebP
        img = Image.open(image_path)
        img = img.convert('RGB')

        webp_path = image_path.rsplit('.', 1)[0] + '.webp'
        img.save(webp_path, format='WEBP', quality=70)

        # 2️⃣ Delete original file
        os.remove(image_path)

        # 3️⃣ Update DB field to point to .webp file
        relative_webp_path = image_field.name.rsplit('.', 1)[0] + '.webp'
        setattr(instance, field_name, relative_webp_path)
        instance.save(update_fields=[field_name])
# 📐 Thumbnail size
THUMBNAIL_SIZE = (300, 300)
MAX_SIZE_MB = 2




def get_file_size_mb(path):
    return os.path.getsize(path) / (1024 * 1024)

def compress_and_thumbnail(image_path):
    """Compress image to WebP and create thumbnail"""
    if not image_path or not os.path.exists(image_path):
        return None, None

    img = Image.open(image_path)
    img = img.convert('RGB')

    # Resize if > 2MB
    if get_file_size_mb(image_path) > MAX_SIZE_MB:
        img.thumbnail((1600, 1600))  

    # WebP compress
    webp_path = image_path.rsplit('.', 1)[0] + '.webp'
    img.save(webp_path, format='WEBP', quality=70)

    # Thumbnail
    thumb_img = img.copy()
    thumb_img.thumbnail(THUMBNAIL_SIZE)
    thumb_path = image_path.rsplit('.', 1)[0] + '_thumb.webp'
    thumb_img.save(thumb_path, format='WEBP', quality=80)

    # Remove original
    os.remove(image_path)

    return webp_path, thumb_path

def process_image_field(instance, field_name):
    image_field = getattr(instance, field_name)
    if image_field and not str(image_field).endswith('.webp'):
        webp_path, thumb_path = compress_and_thumbnail(image_field.path)
        if webp_path:
            relative_webp_path = image_field.name.rsplit('.', 1)[0] + '.webp'
            setattr(instance, field_name, relative_webp_path)
            instance.save(update_fields=[field_name])

# ✅ Project
@receiver(post_save, sender=Project)
def compress_Project_image(sender, instance, **kwargs):
    process_image_field(instance, 'image')

# ✅ Project WebSlider
@receiver(post_save, sender=WebSlider)
def compress_webslider_image(sender, instance, **kwargs):
    process_image_field(instance, 'image')

# ✅ Gallery
@receiver(post_save, sender=Gallery)
def compress_gallery_image(sender, instance, **kwargs):
    process_image_field(instance, 'image')

# ✅ Header (multiple)
@receiver(post_save, sender=Header)
def compress_header_images(sender, instance, **kwargs):
    for field_name in ['logo', 'welcome_to_bg', 'virtual_site_visit_bg', 'schedule_a_site_visit']:
        process_image_field(instance, field_name)

# ✅ RERA Info
@receiver(post_save, sender=RERA_Info)
def compress_rera_image(sender, instance, **kwargs):
    process_image_field(instance, 'qr_image')
