# Generated by Django 3.1.7 on 2021-04-08 10:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('locationsadmin', '0007_property_deposit'),
    ]

    operations = [
        migrations.AddField(
            model_name='property',
            name='CustomerFeast',
            field=models.CharField(choices=[('Any', 'Any'), ('Veg', 'Veg'), ('Non-Veg', 'Non-Veg')], default='', max_length=250, verbose_name='Customer Feast'),
        ),
        migrations.AddField(
            model_name='property',
            name='CustomerStatus',
            field=models.CharField(choices=[('Any', 'Any'), ('Family', 'Family'), ('Bachelor', 'Bachelor')], default='', max_length=250, verbose_name='Customer Status'),
        ),
        migrations.AddField(
            model_name='property',
            name='PetsAllowed',
            field=models.CharField(choices=[('Allowed', 'Allowed'), ('Not Allowed', 'Not Allowed')], default='', max_length=250, verbose_name='Pet Allowed?'),
        ),
        migrations.AddField(
            model_name='property',
            name='RentAmount',
            field=models.FloatField(blank=True, null=True, verbose_name='Price (RENT)'),
        ),
        migrations.AddField(
            model_name='property',
            name='RentPossessionDate',
            field=models.DateField(blank=True, null=True, verbose_name='Rent Possession Date'),
        ),
        migrations.AlterField(
            model_name='property',
            name='Deposit',
            field=models.CharField(blank=True, default='', max_length=250, null=True, verbose_name='Deposit'),
        ),
        migrations.AlterField(
            model_name='property',
            name='PossessionStatus',
            field=models.CharField(choices=[('Ready to Move', 'Ready to Move'), ('Under Construction', 'Under Construction')], default='', max_length=250, verbose_name='Posession Status (Applicable for BUY only)'),
        ),
        migrations.AlterField(
            model_name='property',
            name='Price',
            field=models.FloatField(verbose_name='Price (BUY/RENT)'),
        ),
        migrations.AlterField(
            model_name='property',
            name='TxnType',
            field=models.CharField(choices=[('BUY', 'BUY'), ('RENT', 'RENT')], default='', max_length=200, verbose_name='Transaction Status'),
        ),
    ]
