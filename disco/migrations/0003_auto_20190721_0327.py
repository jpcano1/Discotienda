# Generated by Django 2.2.3 on 2019-07-21 03:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('disco', '0002_auto_20190721_0307'),
    ]

    operations = [
        migrations.AlterField(
            model_name='albumrating',
            name='rated_album',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='rated_album', to='disco.Album'),
        ),
    ]
