# Generated by Django 3.2 on 2021-04-20 11:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('videos', '0004_videoproxy'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='videoproxy',
            options={'verbose_name': 'Published Video', 'verbose_name_plural': 'Published Videos'},
        ),
    ]
