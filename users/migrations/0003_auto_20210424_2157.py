# Generated by Django 3.1.6 on 2021-04-24 16:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_auto_20210424_2151'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='dob',
            field=models.DateField(null=True, verbose_name='Date of Birth'),
        ),
    ]
