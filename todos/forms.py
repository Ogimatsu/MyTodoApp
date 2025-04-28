from django import forms
from .models import Todo

#Todoモデルのフォーム
class TodoForm(forms.ModelForm):
    class Meta:
        model = Todo
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            # フィールドの種類によってクラスをつける（テキストかセレクトかで）
            if isinstance(field.widget, forms.widgets.TextInput) or isinstance(field.widget, forms.widgets.Textarea):
                field.widget.attrs['class'] = 'form-control'
            elif isinstance(field.widget, forms.widgets.Select):
                field.widget.attrs['class'] = 'form-select'
