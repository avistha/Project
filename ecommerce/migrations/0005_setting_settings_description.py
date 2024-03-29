# Generated by Django 4.1.7 on 2023-03-24 06:41

import ckeditor_uploader.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecommerce', '0004_settings'),
    ]

    operations = [
        migrations.CreateModel(
            name='Setting',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
                ('email', models.EmailField(max_length=100, unique=True)),
                ('phone', models.CharField(max_length=100, unique=True)),
                ('address', models.CharField(max_length=100, unique=True)),
                ('logo', models.ImageField(upload_to='media/logo')),
                ('icon', models.ImageField(upload_to='media/icon')),
                ('description', ckeditor_uploader.fields.RichTextUploadingField(blank=True, null=True)),
            ],
        ),
        migrations.AddField(
            model_name='settings',
            name='description',
            field=ckeditor_uploader.fields.RichTextUploadingField(blank=True, null=True),
        ),
    ]
