# Generated by Django 3.0.2 on 2020-02-11 13:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0009_auto_20200211_1321'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='photo',
            field=models.ImageField(default='/profiles/profile.jpg', upload_to='media/profiles'),
        ),
    ]
