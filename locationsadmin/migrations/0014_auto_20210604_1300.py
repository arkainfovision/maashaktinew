# Generated by Django 3.1.7 on 2021-06-04 13:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('locationsadmin', '0013_auto_20210503_1310'),
    ]

    operations = [
        migrations.AlterField(
            model_name='property',
            name='Availability',
            field=models.CharField(blank=True, default='Available', max_length=250, verbose_name='AVAILABLE'),
        ),
        migrations.AlterField(
            model_name='property',
            name='PriceUnit',
            field=models.CharField(choices=[('Cr', 'Cr'), ('Lac', 'Lac'), ('K', 'K')], default='', max_length=250, verbose_name='PRICE UNIT'),
        ),
        migrations.AlterField(
            model_name='property',
            name='PropertyImage',
            field=models.ImageField(default='building.png', upload_to='propertybanner', verbose_name='PROPERTY PROFILE MAIN IMAGE'),
        ),
        migrations.AlterField(
            model_name='property',
            name='RateSQFT',
            field=models.FloatField(blank=True, default='', null=True, verbose_name='RATE PER SQRFT'),
        ),
        migrations.AlterField(
            model_name='property',
            name='RentAmountUnit',
            field=models.CharField(choices=[('Cr', 'Cr'), ('Lac', 'Lac'), ('K', 'K')], default='', max_length=250, verbose_name='AMOUNT UNIT'),
        ),
        migrations.AlterField(
            model_name='property',
            name='ShortDescription',
            field=models.TextField(blank=True, default='', max_length=5000, verbose_name='PROPERTY DESCRIPTION'),
        ),
    ]
