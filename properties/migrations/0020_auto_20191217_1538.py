# Generated by Django 2.2.7 on 2019-12-17 15:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('properties', '0019_auto_20191217_1428'),
    ]

    operations = [
        migrations.AlterField(
            model_name='businesstype',
            name='name',
            field=models.CharField(choices=[('SALE / VENTA', 'sale'), ('RENT / ARRENDAMIENTO', 'rent'), ('SWAP / PERMUTA', 'swap')], default='SALE / VENTA', max_length=70, verbose_name='type of business'),
        ),
        migrations.CreateModel(
            name='Gallery',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('imagen', models.ImageField(blank=True, default='img/img_1.jpg', null=True, upload_to='img/')),
                ('propiedad', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='gallery', to='properties.Property')),
            ],
        ),
    ]