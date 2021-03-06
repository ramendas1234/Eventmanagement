# Generated by Django 2.0.3 on 2020-04-17 07:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0024_auto_20200417_0653'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='image',
            field=models.ImageField(default='', upload_to='catalog/uploads'),
        ),
        migrations.AlterField(
            model_name='category',
            name='description',
            field=models.TextField(default='', help_text='enter category description'),
        ),
        migrations.AlterField(
            model_name='category',
            name='name',
            field=models.CharField(default='', max_length=200),
        ),
    ]
