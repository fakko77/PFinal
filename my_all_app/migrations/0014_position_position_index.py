# Generated by Django 3.2.2 on 2021-09-02 22:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('my_all_app', '0013_index'),
    ]

    operations = [
        migrations.AddField(
            model_name='position',
            name='position_index',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='my_all_app.index'),
        ),
    ]