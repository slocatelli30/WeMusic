# Generated by Django 4.1.4 on 2023-02-25 20:06

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wmapp', '0004_song_file_alter_album_pub_date_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='album',
            name='pub_date',
            field=models.DateTimeField(default=datetime.datetime(2023, 2, 25, 21, 6, 41, 577672), verbose_name='date published'),
        ),
        migrations.AlterField(
            model_name='playlist',
            name='creation_date',
            field=models.DateTimeField(default=datetime.datetime(2023, 2, 25, 21, 6, 41, 577672), verbose_name='creation date'),
        ),
    ]