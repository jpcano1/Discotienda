# Generated by Django 2.2.3 on 2019-07-25 01:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_user_picture'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='picture',
        ),
    ]
