from django.urls import path, include
from django.contrib import admin

urlpatterns = [
    path('api/', include('accounts.urls')),
    path('admin/', admin.site.urls),
]
