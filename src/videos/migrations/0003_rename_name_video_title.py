# Generated by Django 3.2 on 2021-04-20 10:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('videos', '0002_rename_title_video_name'),
    ]

    operations = [
        migrations.RenameField(
            model_name='video',
            old_name='name',
            new_name='title',
        ),
    ]
