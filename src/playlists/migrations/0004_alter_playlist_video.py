# Generated by Django 3.2 on 2021-04-21 11:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('videos', '0012_alter_video_video_id'),
        ('playlists', '0003_auto_20210421_1415'),
    ]

    operations = [
        migrations.AlterField(
            model_name='playlist',
            name='video',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='playlist_featured', to='videos.video'),
        ),
    ]
