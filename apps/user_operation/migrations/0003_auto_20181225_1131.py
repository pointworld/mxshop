# Generated by Django 2.1.4 on 2018-12-25 11:31

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('goods', '0002_auto_20181224_1147'),
        ('user_operation', '0002_auto_20181219_1930'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='userfav',
            unique_together={('user', 'goods')},
        ),
    ]
