# Generated by Django 3.2.10 on 2022-01-07 17:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop_management', '0014_alter_shop_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='shop',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='images/shop_images', verbose_name='عکس فروشگاه'),
        ),
    ]
