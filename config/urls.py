from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('todos/', include('todos.urls')),
    path('admin/', admin.site.urls),
]
