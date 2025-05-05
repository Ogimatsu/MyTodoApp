from datetime import datetime, date
from django import forms
from .models import Todo
from utils.messages_def import MESSAGES

# 目標・実績の入力値チェック
def validate_value_check(field_label):
    def _validate(value):
        # 入力値がマイナスの場合エラー
        if value is not None and value < 0:
            raise forms.ValidationError(MESSAGES["MSG_2104"]["text"].format(field=field_label))
    return _validate


# 日付入力の妥当性チェック
def validate_date_range(date_label):
    def _validate(value):
        if value:
            # datetime型ならdate型に変更する
            if isinstance(value, datetime):
                value = value.date()

            if value.year > 9999:
                # 年が5桁以上の場合エラー
                raise forms.ValidationError(MESSAGES["MSG_2102"]["text"].format(field=date_label))
            elif value < date(1990,1,1):
                # 1990年1月1日以前の日付を入力している場合エラー
                raise forms.ValidationError(MESSAGES["MSG_2103"]["text"].format(field=date_label))
    return _validate

# 日付の開始日と終了日の整合性チェック
def validate_date_pairs(form_instance, cleaned_data, date_pairs):
    for from_key, to_key, label in date_pairs:
        from_date = cleaned_data.get(from_key)
        to_date = cleaned_data.get(to_key)

        if from_date and to_date and from_date > to_date:
            form_instance.add_error(
                from_key,
                MESSAGES["MSG_2101"]["text"].format(field=label)
            )

# 新規作成・編集用フォーム
class TodoForm(forms.ModelForm):
    class Meta:
        model = Todo
        fields = '__all__'
        widgets = {
            # 締切日時は日付の入力欄にする
            'due_date': forms.DateInput(attrs={
                                    'type': 'date',
                                    'min': '1900-01-01',
                                    'max': '9999-12-31',
                                    'class': 'form-control'
                                }),
            # 目標値は数値の入力欄にする（入力値は0以上）
            'target_value': forms.NumberInput(attrs={
                                    'min': 0,
                                    'class': 'form-control'
                                }),
            # 目標値は数値の入力欄にする（入力値は0以上）
            'actual_value': forms.NumberInput(attrs={
                                    'min': 0,
                                    'class': 'form-control'
                                }),
            }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            # 締切日時、目標値、実績値の場合、条件を満たした場合エラーメッセージを表示する。
            if field_name == 'due_date':
                field.validators.append(validate_date_range('締切日時'))
                field.error_messages['invalid'] = MESSAGES["MSG_2102"]["text"].format(field='締切日時')
            elif field_name == 'target_value':
                field.validators.append(validate_value_check('目標値'))
                field.error_messages['invalid'] = MESSAGES["MSG_2104"]["text"].format(field='目標値')
            elif field_name == 'actual_value':
                field.validators.append(validate_value_check('実績値'))
                field.error_messages['invalid'] = MESSAGES["MSG_2104"]["text"].format(field='実績値')

            # フィールドの種類によってクラスをつける（テキストかセレクトかで）
            if isinstance(field.widget, forms.widgets.TextInput) or isinstance(field.widget, forms.widgets.Textarea):
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

# 日時フォーム取得用
def get_date_form(date_label):
    return forms.DateField(required=False,
                        widget=forms.DateInput(attrs={
                            'type': 'date',
                            'min': '1900-01-01',
                            'max': '9999-12-31',
                            'class': 'form-control'
                        }),
                        label=date_label,
                        validators=[validate_date_range(date_label)],
                        error_messages={
                            'invalid': MESSAGES['MSG_2102']['text'].format(field=date_label)
                        }
                    )

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

    def clean(self):
        cleaned_data = super().clean()
        date_pairs = [
            ('updated_from', 'updated_to', '更新'),
            ('created_from', 'created_to', '作成'),
            ('due_date_from', 'due_date_to', '締切'),
            ('completed_from', 'completed_to', '完了'),
        ]
        validate_date_pairs(self,cleaned_data,date_pairs)