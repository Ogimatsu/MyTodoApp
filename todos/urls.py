from django.urls import path
from . import views

app_name = "todos"
urlpatterns = [
    path('', views.index, name='index'), # 一覧表示
    path('create/', views.create, name='create'), # 新規作成ページ
    path('update/<int:pk>/', views.update, name='update'), # 更新ページ
    path('delete/<int:pk>/', views.delete, name='delete'), # 削除ページ
]