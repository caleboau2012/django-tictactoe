# Generated by Django 3.0.2 on 2020-01-04 22:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gameplay', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='game',
            name='status',
            field=models.CharField(default='F', max_length=1),
        ),
    ]