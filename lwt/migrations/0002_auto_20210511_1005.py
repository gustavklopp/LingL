# Generated by Django 3.2 on 2021-05-11 10:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lwt', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='words',
            name='text_order',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterUniqueTogether(
            name='words',
            unique_together={('wordtext', 'sentence', 'order', 'owner')},
        ),
    ]