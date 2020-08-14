# Generated by Django 2.2.6 on 2020-06-15 14:33

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('catalog', '0043_delete_attendee'),
    ]

    operations = [
        migrations.CreateModel(
            name='Attendee',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('attedee_name', models.CharField(default='', max_length=300)),
                ('attendee_email', models.CharField(default='', max_length=100)),
                ('attendee_mobile', models.CharField(default='', max_length=30)),
                ('status', models.BooleanField(default=False)),
                ('event', models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='catalog.Event')),
                ('tickit', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='catalog.Tickit')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]