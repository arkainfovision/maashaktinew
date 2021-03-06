# Generated by Django 3.1.7 on 2021-07-31 10:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('locationsadmin', '0016_eventphotos'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='eventphotos',
            options={'verbose_name': 'EVENT PHOTO', 'verbose_name_plural': 'EVENT PHOTOS'},
        ),
        migrations.AddField(
            model_name='property',
            name='DepositUnit',
            field=models.CharField(blank=True, choices=[('Cr', 'Cr'), ('Lakhs', 'Lakhs'), ('K', 'K')], default='', max_length=250, null=True, verbose_name='DEPOSIT UNIT'),
        ),
    ]
