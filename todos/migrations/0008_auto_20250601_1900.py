from django.db import migrations
from django.contrib.auth import get_user_model

def create_admin_user(apps, schema_editor):
    User = get_user_model()
    if not User.objects.filter(id=1).exists():
        User.objects.create(
            id=1,
            username='admin',
            email='admin@example.com',
            is_staff=True,
            is_superuser=True
        )

class Migration(migrations.Migration):

    dependencies = [
        ('todos', '0007_todo_user'),
    ]

    operations = [
        migrations.RunPython(create_admin_user),
    ]
