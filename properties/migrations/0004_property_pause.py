# Generated by Django 3.0.2 on 2020-02-14 22:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('properties', '0003_auto_20200214_2134'),
    ]

    operations = [
        migrations.AddField(
            model_name='property',
            name='pause',
            field=models.BooleanField(default=False, verbose_name='pause'),
        ),
    ]