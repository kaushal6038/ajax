# Generated by Django 2.2.5 on 2019-09-30 07:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('userauth', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userotp',
            name='otp',
        ),
    ]
