# Generated by Django 5.1.3 on 2025-01-17 14:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0002_member_group_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='member',
            name='location',
            field=models.IntegerField(blank=True, choices=[(1, 'Location 1'), (2, 'Location 2'), (3, 'Location 3')], null=True),
        ),
    ]
