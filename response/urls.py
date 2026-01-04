from django.urls import path
from .views import thank_you, submit_additional_info, submit_configuration, error_page

app_name = "response" 

urlpatterns = [
    path("thank-you.html", thank_you, name="thank_you"),
    path("additional-info/", submit_additional_info, name="additional_info"),
    path("configuration/", submit_configuration, name="configuration"),
    path("error_page/", error_page, name="error_page"),


]
