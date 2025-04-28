from django.db import models

#Todoテーブル
class Todo(models.Model):
    title = models.CharField(max_length=200) #タスク名
    URGENCY_CHOICES = [
        (0,'低'),
        (1,'高')
    ]
    urgency = models.IntegerField(choices=URGENCY_CHOICES,default=0) #緊急度
    IMPORTANCE_CHOICES = [
        (0,'低'),
        (1,'高')
    ]
    importance = models.IntegerField(choices=IMPORTANCE_CHOICES,default=0) #重要度
    target_value = models.IntegerField(default=0, null=True, blank=True) #目標値
    target_unit = models.CharField(max_length=20, null=True, blank=True) #目標単位
    actual_value = models.IntegerField(default=0, null=True, blank=True) #実績値
    STATUS_CHOICES = [
        (0,'着手中'),
        (1,'完了')
    ]
    status = models.IntegerField(choices=STATUS_CHOICES,default=0) #ステータス
    created_at = models.DateTimeField(auto_now_add=True) #作成日時
    updated_at = models.DateTimeField(auto_now=True) #更新日時
    due_date = models.DateTimeField(default=None, null=True, blank=True) #締切日時
    completed_at = models.DateTimeField(default=None, null=True, blank=True) #完了日時

    # タスク名を表示
    def __str__(self):
        return self.title

    # 進捗率の取得
    @property
    def progress_percent(self):
        actual = self.actual_value
        target = self.target_value
        # 実績値はNoneでないこと、目標値はNone及び0でないこと
        if actual is not None and target is not None and target != 0:
            try:
                return int((actual / target) * 100)
            except ZeroDivisionError:
                return 0
        return None

    # 進捗バーの色を取得する処理
    @property
    def get_progressbar_color(self):
        if self.progress_percent is None:
            return 'bg-secondary'
        elif self.progress_percent >= 100:
            return 'bg-success'
        elif self.progress_percent >= 70:
            return 'bg-info'
        elif self.progress_percent >= 30:
            return 'bg-warning'
        else:
            return 'bg-danger'

    # 目標単位が空白の場合は記載しないようにする
    @property
    def unit_display(self):
        if self.target_unit in [None, '']:
            return ''
        return self.target_unit
