# Generated by Django 2.2.3 on 2019-07-22 03:38

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('disco', '0005_auto_20190722_0301'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='album',
            name='sold_by',
        ),
        migrations.AddField(
            model_name='album',
            name='sold_by',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='album_sold_by', to=settings.AUTH_USER_MODEL),
        ),
    ]
