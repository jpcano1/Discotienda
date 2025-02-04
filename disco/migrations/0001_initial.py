# Generated by Django 2.2.3 on 2019-07-19 02:11

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Album',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, help_text='Date time in which the object was created', verbose_name='Created at field')),
                ('modified_at', models.DateTimeField(auto_now=True, help_text='Date time in which the object was modified', verbose_name='Modified at field')),
                ('title', models.CharField(max_length=255)),
                ('artist', models.CharField(max_length=255)),
                ('genre', models.CharField(max_length=20)),
                ('cover', models.ImageField(blank=True, null=True, upload_to='album/covers/')),
                ('price', models.FloatField()),
                ('quantities', models.IntegerField(default=1)),
                ('sold_unities', models.IntegerField(default=0)),
                ('digital', models.BooleanField(default=False)),
                ('sold_by', models.ManyToManyField(related_name='album_sold_by', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-created_at', '-modified_at'],
                'get_latest_by': 'created_at',
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='AlbumRating',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, help_text='Date time in which the object was created', verbose_name='Created at field')),
                ('modified_at', models.DateTimeField(auto_now=True, help_text='Date time in which the object was modified', verbose_name='Modified at field')),
                ('rating', models.FloatField(default=1.0)),
                ('comments', models.TextField(blank=True)),
                ('rated_song', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='rated_song', to='disco.Album')),
                ('rating_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='album_rating_user', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-created_at', '-modified_at', '-rating'],
                'get_latest_by': 'created_at',
                'abstract': False,
            },
        ),
    ]
