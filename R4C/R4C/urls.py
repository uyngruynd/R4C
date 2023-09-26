from django.contrib import admin
from django.urls import path

from robots.views import create, report

urlpatterns = [
    path('robots/create/', create, name='create'),
    path('robots/report/', report, name='report'),
    path('admin/', admin.site.urls),
]
