# Generated by Django 3.2.10 on 2022-01-10 16:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0019_alter_customuser_is_salesman'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='phone_number',
            field=models.CharField(max_length=11, unique=True, verbose_name='شماره موبایل'),
        ),
    ]
