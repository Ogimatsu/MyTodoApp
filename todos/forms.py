from django import forms
from .models import Todo

#Todoモデルのフォーム
class TodoForm(forms.ModelForm):
    class Meta:
        model = Todo
        fields = ['title','urgency','importance','target_value','target_unit','actual_value','due_date','completed']
        labels = {
            'title':'タスク名',
            'urgency':'緊急度',
            'importance':'重要度',
            'target_value':'目標値',
            'target_unit':'目標単位',
            'actual_value':'実績値',
            'due_date':'締切日時',
            'completed':'タスク完了'
        }