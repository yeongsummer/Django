# Generated by Django 3.2.7 on 2021-10-20 15:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_user_following'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='following',
            new_name='followings',
        ),
    ]
