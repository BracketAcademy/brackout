# Generated by Django 3.1.4 on 2021-01-12 18:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0006_user_auth_provider'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='auth_provider',
            field=models.CharField(choices=[('EM', 'email'), ('GO', 'google')], default='email', max_length=255, verbose_name='Auth Provider'),
        ),
    ]
