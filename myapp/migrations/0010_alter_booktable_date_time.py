# Generated by Django 4.0 on 2021-12-15 08:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0009_alter_booktable_date_time_alter_order_table_no'),
    ]

    operations = [
        migrations.AlterField(
            model_name='booktable',
            name='date_time',
            field=models.DateTimeField(verbose_name='book table date'),
        ),
    ]
