# Generated by Django 4.1 on 2022-08-17 00:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('groupChat', '0002_alter_room_options_room_participants'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='message',
            options={'ordering': ['-updated', '-created']},
        ),
        migrations.AddField(
            model_name='topic',
            name='profile',
            field=models.ImageField(default='hello', upload_to='GroupPics'),
            preserve_default=False,
        ),
    ]
