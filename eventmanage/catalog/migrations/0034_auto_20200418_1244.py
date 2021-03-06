# Generated by Django 2.2.6 on 2020-04-18 07:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0033_auto_20200418_0935'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='title',
            field=models.CharField(default='', help_text='Enter event name', max_length=300),
        ),
        migrations.CreateModel(
            name='Tickit',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tickit_name', models.CharField(default='', max_length=200)),
                ('tickit_quantity', models.CharField(default='', max_length=10)),
                ('tickit_type', models.CharField(choices=[('free', 'Free'), ('paid', 'Paid')], default='free', max_length=5)),
                ('payment_currency', models.CharField(choices=[('inr', 'INR(₹)')], max_length=20)),
                ('tickit_price', models.CharField(default='', max_length=100)),
                ('payment_type', models.CharField(choices=[('online', 'Pay Online'), ('venue', 'Pay at Venue')], default='online', max_length=10)),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='catalog.Event')),
            ],
        ),
    ]
