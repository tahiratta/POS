# Generated by Django 2.0.2 on 2018-05-17 13:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0079_sale_product_bill'),
    ]

    operations = [
        migrations.AddField(
            model_name='sale_product',
            name='price',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=15, max_length=200),
        ),
    ]
