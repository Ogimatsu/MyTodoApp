import datetime
from django.db import models
from django.utils import timezone

#Todoテーブル
class Todo(models.Model):
    title = models.CharField(max_length=200) #タスク名
    completed = models.BooleanField(default=False) #完了フラグ
    created_at = models.DateTimeField(auto_now_add=True) #作成日時
    completed_at = models.DateTimeField(default=None, null=True, blank=True) #完了日時

    def __str__(self):
        return self.title
    