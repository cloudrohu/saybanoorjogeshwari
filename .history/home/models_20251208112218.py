from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField
from django.utils.safestring import mark_safe
from utility.compress_mixin import ImageCompressionMixin


# =============================
# 🧠 MAIN MODEL — Website Setting
# =============================
class Setting(ImageCompressionMixin, models.Model):    
    site_name = models.CharField(max_length=150)
    logo = models.ImageField(upload_to='settings/', blank=True, null=True)
    favicon = models.ImageField(upload_to='settings/', blank=True, null=True)
    search_bg = models.ImageField(upload_to='logo/', blank=True, null=True)
    testmonial_bg = models.ImageField(upload_to='logo/')
    header_footer_color = models.CharField(max_length=150, blank=True)
    text_color = models.CharField(max_length=150, blank=True)
    address = models.CharField(blank=True, max_length=100)
    phone = models.CharField(blank=True, max_length=15)
    whatsapp = models.CharField(blank=True, max_length=15)
    email = models.CharField(blank=True, max_length=50)
    google_map = models.CharField(blank=True, max_length=1000)
    smtpserver = models.CharField(blank=True, max_length=50)
    smtpemail = models.CharField(blank=True, max_length=50)
    smtppassword = models.CharField(blank=True, max_length=10)
    smtpport = models.CharField(blank=True, max_length=5)
    meta_title = models.CharField(max_length=200, blank=True, null=True)
    meta_description = models.TextField(blank=True, null=True)
    footer_text = models.CharField(max_length=250, blank=True, null=True)
    copy_right = models.CharField(blank=True, max_length=100)


    STATUS = (
        ('True', 'True'),
        ('False', 'False'),
    )
    
    

    facebook = models.CharField(blank=True, max_length=50)
    instagram = models.CharField(blank=True, max_length=50)
    twitter = models.CharField(blank=True, max_length=50)
    youtube = models.CharField(blank=True, max_length=50)

    status = models.CharField(max_length=10, choices=STATUS)


    class Meta:
        verbose_name_plural = '0. Website Settings'

    def __str__(self):
        return self.site_name

    def logo_tag(self):
        if self.logo:
            return mark_safe(f'<img src="{self.logo.url}" width="100"/>')
        return "(No Logo)"

    @property
    def logo_or_name(self):
        if self.logo and self.logo.name:
            return self.logo.url
        return None



# =============================
# 🖼️ Hero / Slider Section (Multiple)
# =============================
class Slider(models.Model):
    title = models.CharField(max_length=200)
    subtitle = models.CharField(max_length=300, blank=True, null=True)
    image = models.ImageField(upload_to='slider/')
    button_text = models.CharField(max_length=100, blank=True, null=True)
    button_link = models.URLField(blank=True, null=True)
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['order']
        verbose_name_plural = '1. Slider Section'

    def __str__(self):
        return self.title
# =============================
# 👥 Leadership Team Section
# =============================


class Leadership(models.Model):
    name = models.CharField(max_length=100, help_text="Full name of the team member")
    designation = models.CharField(max_length=150, help_text="Position or title (e.g., CEO, Managing Director)")
    image = models.ImageField(upload_to='about/leadership/', help_text="Profile image (recommended size 400x400)")
    bio = models.TextField(blank=True, null=True, help_text="Short bio or description about this leader")
    
    linkedin_url = models.URLField(blank=True, null=True, help_text="Optional LinkedIn profile link")
    email = models.EmailField(blank=True, null=True, help_text="Optional contact email for public display")

    display_order = models.PositiveIntegerField(default=0, help_text="Order of appearance on frontend")
    is_active = models.BooleanField(default=True, help_text="Toggle visibility on frontend")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "3. Leadership Team"
        ordering = ['display_order', 'name']

    def __str__(self):
        return f"{self.name} ({self.designation})"


class Why_Choose(models.Model):
    title = models.CharField(max_length=200)
    subtitle = models.CharField(max_length=300, blank=True, null=True)
    order = models.PositiveIntegerField(default=0, help_text="Order of appearance on frontend")
    is_active = models.BooleanField(default=True, help_text="Toggle visibility on frontend")

    class Meta:
        ordering = ['order']
        verbose_name_plural = '6. Why Choose Section'

    def __str__(self):
        return self.title



class About(models.Model):
    # =============================
    # 🎨 Background / Banner Section
    # =============================
    search_bg = models.ImageField(
        upload_to='about/backgrounds/',
        blank=True, null=True,
        help_text="Background image for the top search banner (optional)"
    )
    home_bg = models.ImageField(
        upload_to='about/backgrounds/',
        blank=True, null=True,
        help_text="Background image for home about section"
    )

    # =============================
    # 🏠 Main About Section
    # =============================
    title = models.CharField(max_length=200, help_text="Main heading (e.g., 'About Makaan Hub')")
    subtitle = models.CharField(max_length=300, blank=True, null=True, help_text="Subtitle or tagline")
    content = RichTextUploadingField(blank=True, null=True, help_text="Detailed About Us content with formatting")
    image = models.ImageField(upload_to='about/', blank=True, null=True, help_text="Main image for About section")

    # =============================
    # 🧑‍💼 Who We Are Section
    # =============================
    who_we_are_title = models.CharField(max_length=200, default="Who We Are")
    who_we_are_subtitle = models.CharField(max_length=300, blank=True, null=True)
    who_we_are_description = RichTextUploadingField(blank=True, null=True, help_text="Description about company identity")

    # =============================
    # 📊 Achievements / Highlights
    # =============================
    projects_delivered = models.PositiveIntegerField(default=0)
    happy_families = models.PositiveIntegerField(default=0)
    years_of_excellence = models.PositiveIntegerField(default=0)
    awards_recognitions = models.PositiveIntegerField(default=0)
    highlight_icon_color = models.CharField(max_length=50, blank=True, null=True, help_text="Optional color for highlight icons (e.g., #0066ff)")

    # =============================
    # 🎯 Mission & Vision
    # =============================
    our_mission_title = models.CharField(max_length=200, default="Our Mission")
    our_mission = RichTextUploadingField(blank=True, null=True)
    our_vision_title = models.CharField(max_length=200, default="Our Vision")
    our_vision = RichTextUploadingField(blank=True, null=True)

    # =============================
    # 💼 Looking To Section
    # =============================
    looking_to_title = models.CharField(max_length=200, help_text="Title for 'Looking To...' section")
    looking_to_description = RichTextUploadingField(blank=True, null=True)
    looking_to_button_text = models.CharField(max_length=50, default="Contact Us", help_text="Call-to-action button text")
    looking_to_button_link = models.URLField(blank=True, null=True, help_text="Button link (e.g., contact page)")

    # =============================
    # 🌐 SEO + Meta Info
    # =============================
    meta_title = models.CharField(max_length=255, blank=True, null=True, help_text="SEO meta title")
    meta_description = models.TextField(blank=True, null=True, help_text="SEO meta description")
    meta_keywords = models.TextField(blank=True, null=True, help_text="SEO keywords separated by commas")

    # =============================
    # ⚙️ Admin Settings
    # =============================
    is_active = models.BooleanField(default=True, help_text="If disabled, this section won't appear on site")
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "2. About Section"
        ordering = ['-created_at']

    def __str__(self):
        return self.title


# =============================
# 📝 Contact Page (Single)
# =============================
class Contact_Page(models.Model):
    heading = models.CharField(max_length=200)
    sub_heading = models.CharField(max_length=300, blank=True, null=True)
    address = models.TextField()
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    map_iframe = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name_plural = '3. Contact Page'

    def __str__(self):
        return self.heading


# =============================
# 👨‍💼 Our Team (Multiple)
# =============================
class Our_Team(models.Model):
    name = models.CharField(max_length=100)
    designation = models.CharField(max_length=100)
    image = models.ImageField(upload_to='team/', blank=True, null=True)
    bio = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name_plural = '4. Our Team'

    def __str__(self):
        return self.name


# =============================
# 💬 Testimonial Section (Multiple)
# =============================
class Testimonial(models.Model):
    name = models.CharField(max_length=100)
    designation = models.CharField(max_length=100, blank=True, null=True)
    message = models.TextField()
    image = models.ImageField(upload_to='testimonial/', blank=True, null=True)
    rating = models.PositiveIntegerField(default=5)

    class Meta:
        verbose_name_plural = '5. Testimonials'

    def __str__(self):
        return f"{self.name} ({self.rating}⭐)"


# =============================
# ❓ FAQ Section (Multiple)
# =============================
class FAQ(models.Model):
    question = models.CharField(max_length=300)
    answer = RichTextUploadingField()

    class Meta:
        verbose_name_plural = '7. FAQ Section'

    def __str__(self):
        return self.question
