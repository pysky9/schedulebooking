# Generated by Django 4.1.5 on 2023-02-28 13:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('calendarApp', '0003_alter_time_pricing_time_setting_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='time_setting',
            name='status',
            field=models.CharField(default='launch', max_length=100),
            preserve_default=False,
        ),
    ]
