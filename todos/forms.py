from django import forms
from .models import Todo

#Todoモデルのフォーム
class TodoForm(forms.ModelForm):
    class Meta:
        model = Todo
        fields = ['title','completed']