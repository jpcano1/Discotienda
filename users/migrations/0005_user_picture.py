# Generated by Django 2.2.3 on 2019-07-25 00:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_auto_20190719_0211'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='picture',
            field=models.ImageField(blank=True, null=True, upload_to='users/pictures/', verbose_name='Profile image'),
        ),
    ]
