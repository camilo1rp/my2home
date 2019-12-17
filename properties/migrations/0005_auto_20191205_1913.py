# Generated by Django 2.2.7 on 2019-12-05 19:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('properties', '0004_auto_20191203_2051'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='property',
            name='type_business',
        ),
        migrations.CreateModel(
            name='BusinessType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('property', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='businesstype', to='properties.Property')),
            ],
        ),
    ]
