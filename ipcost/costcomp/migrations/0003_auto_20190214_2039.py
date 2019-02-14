# Generated by Django 2.1.5 on 2019-02-14 20:39

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('costcomp', '0002_auto_20190214_1629'),
    ]

    operations = [
        migrations.AddField(
            model_name='counsoler',
            name='level',
            field=models.CharField(choices=[('JR', 'Junior'), ('SR', 'Senior')], default='JR', max_length=3),
        ),
        migrations.AlterField(
            model_name='enrollment',
            name='endDate',
            field=models.DateField(default=datetime.date.today),
        ),
        migrations.AlterField(
            model_name='enrollment',
            name='startDate',
            field=models.DateField(default=datetime.date.today),
        ),
    ]