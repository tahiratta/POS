# Generated by Django 2.0.2 on 2018-05-10 11:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0073_remove_product_discount'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='supplier',
        ),
        migrations.RemoveField(
            model_name='purchase',
            name='balance',
        ),
        migrations.RemoveField(
            model_name='purchase',
            name='product',
        ),
        migrations.AddField(
            model_name='product',
            name='purchase',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='blog.Purchase'),
            preserve_default=False,
        ),
    ]
