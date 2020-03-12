# Generated by Django 3.0.2 on 2020-03-02 13:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('properties', '0006_contact_created'),
    ]

    operations = [
        migrations.AddField(
            model_name='property',
            name='condition',
            field=models.CharField(choices=[('NEW', 'new'), ('PLA', 'off-plans'), ('STA', 'on construction'), ('USA', 'used')], default='NEW', max_length=40, verbose_name='condition'),
        ),
    ]
