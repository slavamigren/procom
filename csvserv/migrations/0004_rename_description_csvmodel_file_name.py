# Generated by Django 4.2.5 on 2023-09-08 09:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('csvserv', '0003_alter_csvmodel_description'),
    ]

    operations = [
        migrations.RenameField(
            model_name='csvmodel',
            old_name='description',
            new_name='file_name',
        ),
    ]