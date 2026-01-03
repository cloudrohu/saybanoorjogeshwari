from django.contrib import admin
from .models import (
    Setting, Slider, Leadership, Why_Choose,
    About, Contact_Page, Our_Team, Testimonial, FAQ
)


# =============================
# 🌐 WEBSITE SETTINGS ADMIN
# =============================
@admin.register(Setting)
class SettingAdmin(admin.ModelAdmin):
    list_display = ("site_name", "status", "phone", "email", "logo_preview")
    list_filter = ("status",)
    search_fields = ("site_name", "email", "phone")
    readonly_fields = ("logo_preview",)

    fieldsets = (
        ("🧠 Basic Info", {
            "fields": ("site_name", "logo", "favicon", "logo_preview")
        }),

        ("🎨 Theme Colors", {
            "fields": (
                "header_footer_color",
                "text_color",
                "button_color",
                "rera_color",
            )
        }),

        ("📍 Contact Details", {
            "fields": (
                "address",
                "phone",
                "whatsapp",
                "email",
                "google_map"
            )
        }),

        ("✉️ SMTP Settings", {
            "fields": ("smtpserver", "smtpemail", "smtppassword", "smtpport")
        }),

        ("🌐 Social Links", {
            "fields": ("facebook", "instagram", "twitter", "youtube")
        }),

        ("🔍 SEO & Footer", {
            "fields": ("meta_title", "meta_description", "footer_text", "copy_right")
        }),

        ("⚙️ Other Settings", {
            "fields": (
                "search_bg",
                "testmonial_bg",
                "rera_number",
                "status",
            )
        }),
    )

    def logo_preview(self, obj):
        if obj.logo:
            return f'<img src="{obj.logo.url}" width="80" style="border-radius:6px;">'
        return "No Logo"

    logo_preview.allow_tags = True
    logo_preview.short_description = "Logo Preview"


# =============================
# 🖼️ SLIDER ADMIN
# =============================
@admin.register(Slider)
class SliderAdmin(admin.ModelAdmin):
    list_display = ("title", "order", "is_active")
    list_editable = ("order", "is_active")
    search_fields = ("title", "subtitle")
    ordering = ("order",)
    list_filter = ("is_active",)


# =============================
# 💡 WHY CHOOSE US ADMIN
# =============================
@admin.register(Why_Choose)
class WhyChooseAdmin(admin.ModelAdmin):
    list_display = ("title", "subtitle")
    search_fields = ("title", "subtitle")


# =============================
# 👥 LEADERSHIP TEAM ADMIN
# =============================
@admin.register(Leadership)
class LeadershipAdmin(admin.ModelAdmin):
    list_display = ("name", "designation", "display_order", "is_active")
    list_editable = ("display_order", "is_active")
    search_fields = ("name", "designation")
    list_filter = ("is_active",)
    ordering = ("display_order",)
    readonly_fields = ("created_at", "updated_at")

    fieldsets = (
        ("👤 Profile Info", {"fields": ("name", "designation", "image", "bio")}),
        ("🔗 Links", {"fields": ("linkedin_url", "email")}),
        ("⚙️ Settings", {"fields": ("display_order", "is_active", "created_at", "updated_at")}),
    )


# =============================
# ℹ️ ABOUT PAGE ADMIN
# =============================
@admin.register(About)
class AboutAdmin(admin.ModelAdmin):
    list_display = ("title", "is_active", "created_at", "updated_at")
    list_filter = ("is_active",)
    search_fields = ("title", "meta_title", "meta_keywords")
    readonly_fields = ("created_at", "updated_at")

    fieldsets = (
        ("🏠 Main Section", {"fields": ("title", "subtitle", "content", "image")}),
        ("👥 Who We Are", {"fields": ("who_we_are_title", "who_we_are_subtitle", "who_we_are_description")}),
        ("📊 Highlights", {"fields": (
            "projects_delivered",
            "happy_families",
            "years_of_excellence",
            "awards_recognitions",
            "highlight_icon_color"
        )}),
        ("🎯 Mission & Vision", {"fields": (
            "our_mission_title", "our_mission",
            "our_vision_title", "our_vision"
        )}),
        ("💼 Looking To Section", {"fields": (
            "looking_to_title", "looking_to_description",
            "looking_to_button_text", "looking_to_button_link"
        )}),
        ("🌐 SEO", {"fields": ("meta_title", "meta_description", "meta_keywords")}),
        ("⚙️ Settings", {"fields": ("home_bg", "search_bg", "is_active", "created_at", "updated_at")}),
    )


# =============================
# 📞 CONTACT PAGE ADMIN
# =============================
@admin.register(Contact_Page)
class ContactPageAdmin(admin.ModelAdmin):
    list_display = ("heading", "phone", "email")
    search_fields = ("heading", "email", "phone")
    fieldsets = (
        ("📍 Contact Info", {"fields": ("heading", "sub_heading", "address", "phone", "email")}),
        ("🗺️ Map Integration", {"fields": ("map_iframe",)}),
    )


# =============================
# 👨‍💼 OUR TEAM ADMIN
# =============================
@admin.register(Our_Team)
class OurTeamAdmin(admin.ModelAdmin):
    list_display = ("name", "designation")
    search_fields = ("name", "designation")
    list_filter = ("designation",)


# =============================
# 💬 TESTIMONIAL ADMIN
# =============================
@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ("name", "designation", "rating")
    list_filter = ("rating",)
    search_fields = ("name", "designation", "message")
    ordering = ("-rating",)


# =============================
# ❓ FAQ ADMIN
# =============================
@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ("question",)
    search_fields = ("question", "answer")
