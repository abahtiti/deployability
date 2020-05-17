# Generated by Django 2.2 on 2020-05-17 21:24

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('campaigngenerator', '0003_knownproblems'),
    ]

    operations = [
        migrations.AddField(
            model_name='knownproblems',
            name='fix',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='blocker',
            name='duedate',
            field=models.DateTimeField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
