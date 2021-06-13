# Generated by Django 3.2.4 on 2021-06-06 12:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lwt', '0002_alter_words_text'),
    ]

    operations = [
        migrations.AddField(
            model_name='texts',
            name='wordcount',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='texts',
            name='wordcount_distinct',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='words',
            name='status',
            field=models.IntegerField(choices=[(0, 'Unknown <small>[0]</small>'), (1, 'Learning <small>[1 to 99]</small>'), (100, 'Well-known <small>[100]</small>'), (101, 'Ignored <small>[101]</small>')], default=0),
        ),
    ]