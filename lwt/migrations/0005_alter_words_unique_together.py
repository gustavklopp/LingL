# Generated by Django 3.2 on 2021-05-11 14:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lwt', '0004_auto_20210511_1404'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='words',
            unique_together=set(),
        ),
    ]