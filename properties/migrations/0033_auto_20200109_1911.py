# Generated by Django 2.2.8 on 2020-01-09 19:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('properties', '0032_auto_20200109_1658'),
    ]

    operations = [
        migrations.AlterField(
            model_name='property',
            name='upload_code',
            field=models.IntegerField(blank=True, default=0, null=True, verbose_name='upload-code'),
        ),
    ]
