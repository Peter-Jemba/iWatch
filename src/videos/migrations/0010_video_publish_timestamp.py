# Generated by Django 3.2 on 2021-04-20 13:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('videos', '0009_video_state'),
    ]

    operations = [
        migrations.AddField(
            model_name='video',
            name='publish_timestamp',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
