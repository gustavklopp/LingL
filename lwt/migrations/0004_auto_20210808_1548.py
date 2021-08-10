# Generated by Django 3.2.4 on 2021-08-08 15:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lwt', '0003_auto_20210808_0758'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='equiv_wordtag_oldlwtid_linglid',
            name='owner',
        ),
        migrations.AddField(
            model_name='words',
            name='oldlwtid',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='wordtags',
            name='oldlwtid',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.DeleteModel(
            name='Equiv_word_oldlwtid_linglid',
        ),
        migrations.DeleteModel(
            name='Equiv_wordtag_oldlwtid_linglid',
        ),
    ]
