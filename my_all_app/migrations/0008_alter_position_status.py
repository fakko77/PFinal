# Generated by Django 3.2.3 on 2021-07-08 12:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('my_all_app', '0007_position_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='position',
            name='status',
            field=models.CharField(max_length=20, null=True),
        ),
    ]