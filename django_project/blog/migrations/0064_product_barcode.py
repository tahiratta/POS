# Generated by Django 2.0.2 on 2018-05-03 10:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0063_remove_invoice_product'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='barcode',
            field=models.CharField(default=0, max_length=200),
        ),
    ]
