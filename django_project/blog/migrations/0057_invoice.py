# Generated by Django 2.0.2 on 2018-04-26 09:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0056_remove_purchase_temp'),
    ]

    operations = [
        migrations.CreateModel(
            name='Invoice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='blog.Customer')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='blog.Product')),
                ('sale', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='blog.Sale')),
            ],
        ),
    ]
