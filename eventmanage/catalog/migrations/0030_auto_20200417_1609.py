# Generated by Django 2.0.3 on 2020-04-17 16:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0029_auto_20200417_1603'),
    ]

    operations = [
        migrations.AlterField(
            model_name='image',
            name='event',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='catalog.Event'),
        ),
    ]
