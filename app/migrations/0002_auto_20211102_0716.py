# Generated by Django 3.2.9 on 2021-11-02 07:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='neighbourhood',
            name='health_tell',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='neighbourhood',
            name='police_number',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
