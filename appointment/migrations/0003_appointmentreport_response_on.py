# Generated by Django 3.1.6 on 2021-04-21 13:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('appointment', '0002_auto_20210421_1858'),
    ]

    operations = [
        migrations.AddField(
            model_name='appointmentreport',
            name='response_on',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='appointment.appointment'),
        ),
    ]
