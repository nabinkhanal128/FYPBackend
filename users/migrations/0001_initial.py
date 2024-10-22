# Generated by Django 3.1.6 on 2021-04-10 07:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CustomUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('email', models.EmailField(max_length=255, unique=True, verbose_name='email address')),
                ('first_name', models.CharField(max_length=255, verbose_name='First Name')),
                ('last_name', models.CharField(max_length=255, verbose_name='Last Name')),
                ('phone_number', models.IntegerField(null=True, verbose_name='Phone Number')),
                ('dob', models.DateField(verbose_name='Date of Birth')),
                ('address', models.TextField(max_length=255, verbose_name='Address')),
                ('gender_type', models.CharField(choices=[('M', 'Male'), ('F', 'Female'), ('U', 'Unspecified')], default='F', max_length=10)),
                ('user_type', models.CharField(choices=[('P', 'Patient'), ('D', 'Doctor')], default='P', max_length=10)),
                ('is_verified', models.BooleanField(default=False)),
                ('is_patient', models.BooleanField(default=True)),
                ('is_doctor', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=True)),
                ('is_admin', models.BooleanField(default=False)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Doctor',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, related_name='doctor', serialize=False, to='users.customuser')),
                ('profile_pic', models.ImageField(upload_to='doctorprofile/', verbose_name='Doctor Profile Picture')),
                ('approved', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
                ('specialization', models.CharField(max_length=25)),
                ('about', models.CharField(max_length=1000)),
            ],
        ),
        migrations.CreateModel(
            name='Patient',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, related_name='patient', serialize=False, to='users.customuser')),
                ('blood_type', models.CharField(choices=[('Choose', 'Choose your blood group'), ('A+', 'A+'), ('O+', 'B+'), ('AB+', 'AB+'), ('A-', 'A-'), ('O-', 'O-'), ('B-', 'B-'), ('AB-', 'AB-')], default='Choose', max_length=10)),
                ('profile_pic', models.ImageField(upload_to='patientprofile/', verbose_name='Profile Picture')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
