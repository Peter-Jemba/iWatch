# Generated by Django 3.2 on 2021-04-23 11:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('playlists', '0012_movieproxy'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='movieproxy',
            options={'verbose_name': 'Movie', 'verbose_name_plural': 'Movies'},
        ),
    ]
