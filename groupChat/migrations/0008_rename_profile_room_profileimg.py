# Generated by Django 4.1 on 2022-08-17 00:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('groupChat', '0007_alter_room_profile'),
    ]

    operations = [
        migrations.RenameField(
            model_name='room',
            old_name='profile',
            new_name='profileImg',
        ),
    ]