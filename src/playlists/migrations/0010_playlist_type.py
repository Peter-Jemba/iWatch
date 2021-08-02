# Generated by Django 3.2 on 2021-04-23 08:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('playlists', '0009_tvshowproxy_tvshowseasonproxy'),
    ]

    operations = [
        migrations.AddField(
            model_name='playlist',
            name='type',
            field=models.CharField(choices=[('MOV', 'Movie'), ('TVS', 'TV Show'), ('SEA', 'Season'), ('PLY', 'Playlist')], default='PLY', max_length=3),
        ),
    ]