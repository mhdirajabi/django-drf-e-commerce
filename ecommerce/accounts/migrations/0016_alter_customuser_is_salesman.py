# Generated by Django 3.2.10 on 2022-01-04 15:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0015_auto_20220104_1825'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='is_salesman',
            field=models.BooleanField(blank=True, default=False, verbose_name='فروشنده'),
        ),
    ]
