# Generated by Django 4.0.5 on 2022-07-11 07:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0005_author_book'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='book',
            name='author_name',
        ),
        migrations.DeleteModel(
            name='Author',
        ),
        migrations.DeleteModel(
            name='Book',
        ),
    ]
