# Generated by Django 3.1.7 on 2021-04-27 11:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('locationsadmin', '0009_auto_20210427_1052'),
    ]

    operations = [
        migrations.AddField(
            model_name='property',
            name='RentAmountUnit',
            field=models.CharField(choices=[('Cr', 'Cr'), ('L', 'L'), ('K', 'K')], default='', max_length=250, verbose_name='AMOUNT UNIT'),
        ),
    ]
