# Generated by Django 2.1.3 on 2018-12-01 19:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('poll', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='pollvote',
            name='ip',
            field=models.CharField(blank=True, default='', max_length=100),
        ),
    ]
