# Generated by Django 4.1 on 2022-08-17 08:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('groupChat', '0010_alter_room_name_alter_topic_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='room',
            name='profileImg',
            field=models.ImageField(default='cover_img.jpg', upload_to='GroupPics'),
        ),
    ]
