# Generated by Django 3.2.8 on 2022-01-02 04:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pics', '0007_alter_category_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='name',
            field=models.CharField(max_length=300),
        ),
    ]
