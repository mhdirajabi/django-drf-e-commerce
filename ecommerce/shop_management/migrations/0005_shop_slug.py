# Generated by Django 4.0 on 2021-12-29 12:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop_management', '0004_alter_shop_created_at_alter_shop_last_updated'),
    ]

    operations = [
        migrations.AddField(
            model_name='shop',
            name='slug',
            field=models.SlugField(allow_unicode=True, blank=True, null=True),
        ),
    ]
