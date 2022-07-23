# Generated by Django 3.2.10 on 2022-01-15 13:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop_management', '0018_alter_product_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='is_available',
            field=models.BooleanField(blank=True, null=True, verbose_name='موجود بودن'),
        ),
        migrations.AlterField(
            model_name='product',
            name='price',
            field=models.PositiveIntegerField(verbose_name='قیمت محصول'),
        ),
        migrations.AlterField(
            model_name='product',
            name='stock',
            field=models.PositiveIntegerField(verbose_name='موجودی محصول'),
        ),
    ]
