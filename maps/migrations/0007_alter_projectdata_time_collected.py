# Generated by Django 4.0.3 on 2022-05-06 07:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('maps', '0006_alter_project_last_updated'),
    ]

    operations = [
        migrations.AlterField(
            model_name='projectdata',
            name='time_collected',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
