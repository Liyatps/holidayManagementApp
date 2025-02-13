from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    # path('admin/', admin.site.urls),
    path('holidays/', views.get_holidays, name='get_holidays'),
    path('holidays/search/', views.search_holidays, name='search_holidays'),

    
    
]