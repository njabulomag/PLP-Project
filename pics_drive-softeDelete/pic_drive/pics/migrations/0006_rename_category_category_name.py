# Generated by Django 3.2.8 on 2022-01-01 11:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pics', '0005_remove_picture_name'),
    ]

    operations = [
        migrations.RenameField(
            model_name='category',
            old_name='category',
            new_name='name',
        ),
    ]
