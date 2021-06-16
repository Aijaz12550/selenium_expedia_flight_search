from django.contrib import admin
from django.urls import path
from flight_crawler import expedia
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', expedia.expedia_flights),
    path('flight/crawler', expedia.expedia_flights)
]
