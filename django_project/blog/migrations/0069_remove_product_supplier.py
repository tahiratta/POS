# Generated by Django 2.0.2 on 2018-05-04 09:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0068_product_supplier'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='supplier',
        ),
    ]
