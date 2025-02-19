# Generated by Django 5.1.4 on 2025-01-06 06:03

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RenameField(
            model_name='item',
            old_name='todolst',
            new_name='todolist',
        ),
        migrations.AddField(
            model_name='todolist',
            name='user',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='item',
            name='complete',
            field=models.BooleanField(default=False),
        ),
    ]
