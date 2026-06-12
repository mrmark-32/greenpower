from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Store App URLs
    path('', include('store.urls')),   # ← This is the most important line
]