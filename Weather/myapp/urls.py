from django.urls import path
from .import views
app_name="myapp"

urlpatterns = [
    path('',views.HOME, name="City_weather"),
    path('remove/<city_name>/',views.City_delete, name="City_Remove"),
]
