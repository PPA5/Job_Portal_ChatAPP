# Generated by Django 4.0.5 on 2022-07-31 15:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chatapp', '0005_userchatmessage_timestamp'),
    ]

    operations = [
        migrations.AddField(
            model_name='userchatmessage',
            name='edited',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='userchatmessage',
            name='timestamp',
            field=models.FloatField(default=1659281750.1472528),
        ),
    ]
