# Generated by Django 4.1 on 2022-08-17 00:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('groupChat', '0006_alter_room_profile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='room',
            name='profile',
            field=models.ImageField(default='l', upload_to='GroupPics'),
            preserve_default=False,
        ),
    ]