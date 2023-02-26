# Generated by Django 4.1.4 on 2022-12-28 19:45

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wmapp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='album',
            name='pub_date',
            field=models.DateTimeField(default=datetime.datetime(2022, 12, 28, 20, 45, 6, 699017), verbose_name='date published'),
        ),
        migrations.AlterField(
            model_name='ordinaryuser',
            name='friends',
            field=models.ManyToManyField(blank=True, to='wmapp.ordinaryuser'),
        ),
        migrations.AlterField(
            model_name='ordinaryuser',
            name='liked_songs',
            field=models.ManyToManyField(blank=True, to='wmapp.song'),
        ),
        migrations.AlterField(
            model_name='playlist',
            name='creation_date',
            field=models.DateTimeField(default=datetime.datetime(2022, 12, 28, 20, 45, 6, 700158), verbose_name='creation date'),
        ),
    ]