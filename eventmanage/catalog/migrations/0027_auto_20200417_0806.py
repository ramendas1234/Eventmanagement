# Generated by Django 2.0.3 on 2020-04-17 08:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0026_event_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='banner_image',
            field=models.ImageField(default='', upload_to='catalog/uploads'),
        ),
        migrations.AddField(
            model_name='event',
            name='thumb_image',
            field=models.ImageField(default='', upload_to='catalog/uploads'),
        ),
    ]
