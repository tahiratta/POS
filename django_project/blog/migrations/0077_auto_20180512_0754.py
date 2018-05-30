# Generated by Django 2.0.2 on 2018-05-12 14:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0076_product_bill'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='cost',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=15, max_length=200),
        ),
        migrations.AlterField(
            model_name='product',
            name='quantity',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='product',
            name='salePrice',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=15, max_length=200),
        ),
    ]