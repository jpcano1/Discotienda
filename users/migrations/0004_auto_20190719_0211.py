# Generated by Django 2.2.3 on 2019-07-19 02:11

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_userrating'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userrating',
            name='rated_user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='rated_user', to=settings.AUTH_USER_MODEL),
        ),
    ]
