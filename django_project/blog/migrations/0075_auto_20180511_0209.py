# Generated by Django 2.0.2 on 2018-05-11 09:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0074_auto_20180510_0421'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='purchase',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='blog.Purchase'),
        ),
    ]
