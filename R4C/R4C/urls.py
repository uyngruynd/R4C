from django.contrib import admin
from django.urls import path
from robots.views import create


urlpatterns = [
    path('robots/create/', create, name='create'),
    path('admin/', admin.site.urls),
]