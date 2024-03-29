# Generated by Django 4.1.4 on 2023-08-25 15:28

import cloudinary.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0003_alter_post_post_img_alter_user_avatar_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='avatar',
            field=cloudinary.models.CloudinaryField(default='avatar.png', max_length=255, verbose_name='image'),
        ),
    ]
