# Generated by Django 5.2 on 2025-06-29 07:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('todos', '0008_alter_todo_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='todo',
            name='status',
            field=models.IntegerField(choices=[(0, '進行中'), (1, '完了')], default=0),
        ),
    ]
