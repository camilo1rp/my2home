# Generated by Django 2.2.7 on 2020-01-02 16:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('properties', '0028_auto_20200102_1640'),
    ]

    operations = [
        migrations.AlterField(
            model_name='addresscol',
            name='barrio',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
    ]