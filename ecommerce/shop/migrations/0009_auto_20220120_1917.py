# Generated by Django 3.2.10 on 2022-01-20 15:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0008_alter_cart_shop'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cartitem',
            name='price',
            field=models.PositiveIntegerField(blank=True, verbose_name='قیمت'),
        ),
        migrations.AlterField(
            model_name='cartitem',
            name='quantity',
            field=models.PositiveIntegerField(default=1, verbose_name='تعداد'),
        ),
    ]