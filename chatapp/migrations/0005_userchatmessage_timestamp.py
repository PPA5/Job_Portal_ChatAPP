# Generated by Django 4.0.5 on 2022-07-31 09:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chatapp', '0004_remove_userchatmessage_timestamp'),
    ]

    operations = [
        migrations.AddField(
            model_name='userchatmessage',
            name='timestamp',
            field=models.FloatField(default=1659260955.5027697),
        ),
    ]