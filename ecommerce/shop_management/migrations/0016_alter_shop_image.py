# Generated by Django 3.2.10 on 2022-01-07 17:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop_management', '0015_shop_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shop',
            name='image',
            field=models.ImageField(blank=True, help_text='ارسال عکس اختیاری است.', null=True, upload_to='images/shop_images', verbose_name='عکس فروشگاه'),
        ),
    ]