# Generated by Django 4.1.7 on 2023-03-26 11:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecommerce', '0007_order'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='product_id',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='order',
            name='quantity',
            field=models.IntegerField(null=True),
        ),
    ]
