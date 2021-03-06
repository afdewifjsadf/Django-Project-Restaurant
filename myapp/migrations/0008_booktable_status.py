# Generated by Django 4.0 on 2021-12-11 10:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0007_booktable_date_created_alter_booktable_date_time_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='booktable',
            name='status',
            field=models.CharField(choices=[('Pending', 'Pending'), ('Processing', 'Processing'), ('Complete', 'Complete'), ('Canceled', 'Canceled')], default=7, max_length=30),
            preserve_default=False,
        ),
    ]
