# Generated by Django 4.1 on 2022-08-17 08:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('groupChat', '0009_alter_room_name_alter_topic_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='room',
            name='name',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='topic',
            name='name',
            field=models.CharField(max_length=100),
        ),
    ]