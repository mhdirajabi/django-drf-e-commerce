# Generated by Django 3.2.10 on 2022-01-17 20:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0023_alter_customuser_phone_number'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='bio',
            field=models.TextField(blank=True, null=True, verbose_name='درباره من'),
        ),
    ]
