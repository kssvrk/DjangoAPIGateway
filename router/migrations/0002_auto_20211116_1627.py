# Generated by Django 3.1.11 on 2021-11-16 16:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('router', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='gatewayroute',
            name='activate',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='gatewayroute',
            name='timeout',
            field=models.IntegerField(default=10),
        ),
        migrations.AlterUniqueTogether(
            name='gatewayroute',
            unique_together={('endpoint', 'targeturl')},
        ),
    ]
