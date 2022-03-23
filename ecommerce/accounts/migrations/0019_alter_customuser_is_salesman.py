# Generated by Django 3.2.10 on 2022-01-07 10:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0018_alter_customuser_is_salesman'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='is_salesman',
            field=models.BooleanField(default=False, help_text='اگر مایل به ثبت فروشگاه و همکاری با مکتب هستید این تیک را بزنید.', verbose_name='فروشنده'),
        ),
    ]