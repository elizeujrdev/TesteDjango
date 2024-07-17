from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('', include('fin_analysis.urls'), name='home'),
    path('admin/', admin.site.urls)
]


