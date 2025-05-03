from django import forms
from .models import Todo

# 新規作成・編集用フォーム
class TodoForm(forms.ModelForm):
    class Meta:
        model = Todo
        fields = '__all__'
        widgets = {
            # 締切日時は日付の入力欄にする
            'due_date': forms.DateInput(attrs={
                                    'type': 'date',
                                    'max': '9999-12-31',
                                    'class': 'form-control'})
            }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            # フィールドの種類によってクラスをつける（テキストかセレクトかで）
            if field_name == 'due_date':
                continue
            elif isinstance(field.widget, forms.widgets.TextInput) or isinstance(field.widget, forms.widgets.Textarea):
                field.widget.attrs['class'] = 'form-control'
            elif isinstance(field.widget, forms.widgets.Select):
                field.widget.attrs['class'] = 'form-select'

# 選択フォーム取得用
def get_choice_form(choice_menu,choice_label):
    return forms.ChoiceField(required=False,
                        choices=choice_menu,
                        label=choice_label,
                        widget=forms.Select(attrs={'class':'form-select'})
                    )

# 年が4桁以内かを確認する
def validate_year_within_limit(value):
    if value and value.year > 9999:
        raise forms.ValidationError("年は4桁以内で入力してください。")

# 日時フォーム取得用
def get_date_form(date_label):
    return forms.DateField(required=False,
                        widget=forms.DateInput(attrs={
                            'type': 'date',
                            'max': '9999-12-31',
                            'class': 'form-control'
                        }),
                        label=date_label,
                        validators=[validate_year_within_limit]
                    )

# ソート検索用フォーム
class TodoSearchForm(forms.Form):
    # タスク名
    title = forms.CharField(required=False, label='タスク名', widget=forms.TextInput(attrs={'class':'form-control'}))
    # 緊急度
    urgency = get_choice_form([('', '-----'), (0, '低'), (1, '高')],'緊急度')
    # 重要度
    importance = get_choice_form([('', '-----'), (0, '低'), (1, '高')], '重要度')
    # タスク状態
    status = get_choice_form([('', '-----'), (0, '未完了'), (1, '完了')], 'タスク状態')
    # 更新日時
    updated_from = get_date_form('更新日時（開始）')
    updated_to = get_date_form('更新日時（終了）')
    # 作成日時
    created_from = get_date_form('作成日時（開始）')
    created_to = get_date_form('作成日時（終了）')
    # 締切日時
    due_date_from = get_date_form('締切日時（開始）')
    due_date_to = get_date_form('締切日時（終了）')
    # 完了日時
    completed_from = get_date_form('完了日時（開始）')
    completed_to = get_date_form('完了日時（終了）')
