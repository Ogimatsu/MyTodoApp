from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('',include('users.urls')),
    path('todos/', include('todos.urls', namespace='todos')),
    path('admin/', admin.site.urls),
]
