# Generated by Django 3.2.4 on 2021-06-27 05:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lwt', '0012_auto_20210624_1730'),
    ]

    operations = [
        migrations.AlterField(
            model_name='texts',
            name='contenttype',
            field=models.CharField(blank=True, choices=[('text', 'text'), ('doc', 'doc'), ('html', 'html')], default='text', max_length=4, null=True),
        ),
    ]