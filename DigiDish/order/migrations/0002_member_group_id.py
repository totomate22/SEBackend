# Generated by Django 5.1.3 on 2025-01-17 12:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='member',
            name='group_id',
            field=models.IntegerField(default=0),
        ),
    ]
