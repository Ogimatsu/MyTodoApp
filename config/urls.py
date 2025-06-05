from django.contrib import admin
from django.urls import include, path
from todos.views import index

urlpatterns = [
    path('', index, name='index'),
    path('todos/', include('todos.urls', namespace='todos')),
    path('admin/', admin.site.urls),
    path('', include('users.urls')),
]
