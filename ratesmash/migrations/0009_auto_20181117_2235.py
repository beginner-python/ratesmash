# Generated by Django 2.1.2 on 2018-11-17 22:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ratesmash', '0008_auto_20181117_2156'),
    ]

    operations = [
        migrations.AddField(
            model_name='room',
            name='rate_o',
            field=models.IntegerField(blank=True, default=1500),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='room',
            name='rate_p',
            field=models.IntegerField(blank=True, default=1500),
            preserve_default=False,
        ),
    ]