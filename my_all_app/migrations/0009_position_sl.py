# Generated by Django 3.2.3 on 2021-07-21 09:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('my_all_app', '0008_alter_position_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='position',
            name='sl',
            field=models.FloatField(null=True),
        ),
    ]
