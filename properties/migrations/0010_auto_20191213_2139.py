# Generated by Django 2.2.7 on 2019-12-13 21:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('properties', '0009_remove_businesstype_property'),
    ]

    operations = [
        migrations.AddField(
            model_name='property',
            name='type_business',
            field=models.CharField(default='none', max_length=50, verbose_name='type of business'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='businesstype',
            name='name',
            field=models.CharField(max_length=50, verbose_name='type of property'),
        ),
    ]