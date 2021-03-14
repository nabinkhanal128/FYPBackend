from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse
from django_rest_passwordreset.signals import reset_password_token_created
from django.core.mail import send_mail


@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):

    email_plaintext_message = "{}?token={}".format(reverse('password_reset:reset-password-request'), reset_password_token.key)

    send_mail(
        # title:
        "Password Reset for {title}".format(title="Some website title"),
        # message:
        email_plaintext_message,
        # from:
        "noreply@somehost.local",
        # to:
        [reset_password_token.user.email]
    )

class MyUserManager(BaseUserManager):
    def create_user(self, email, password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
        )
        
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        user = self.create_user(
            email,
            password=password,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class CustomUser(AbstractBaseUser):
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )

    first_name = models.CharField(
        max_length=255,
        verbose_name="First Name",
    )

    last_name = models.CharField(
        max_length=255,
        verbose_name="Last Name",
    )
    user_type_data = (('P', "Patient"), ('D', "Doctor"))
    user_type = models.CharField(default='P', choices=user_type_data, max_length=10)
    is_verified = models.BooleanField(default=False)
    is_patient = models.BooleanField(default=True)
    is_doctor = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = MyUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin

    @property
    def is_superuser(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin

class Patient(models.Model):
    user = models.OneToOneField(
        CustomUser,
        on_delete=models.CASCADE,
        primary_key=True,
        related_name='patient'
    )
    address = models.TextField(
        max_length=255,
        verbose_name="Address", )
    profile_pic = models.ImageField(
        verbose_name="Profile Picture",
    )
    phone_number = models.IntegerField(
        null=True,
        verbose_name="Phone Number",
    )
    dob = models.DateField(
        verbose_name="Date of Birth",
    )
    gender_type_data = (('M', "Male"), ('F', "Female"), ('U', "Unspecified"))
    gender_type = models.CharField(default='F', choices=gender_type_data, max_length=10)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f'{self.user}'

class Doctor(models.Model):
    user = models.OneToOneField(
        CustomUser,
        on_delete=models.CASCADE,
        primary_key=True,
        related_name='doctor'
    )
    address = models.TextField(
        max_length=255,
        verbose_name="Address", )
    profile_pic = models.ImageField(
        verbose_name="Profile Picture",
    )
    phone_number = models.IntegerField(
        null=True,
        verbose_name="Phone Number",
    )
    dob = models.DateField(
        verbose_name="Date of Birth",
    )
    gender_type_data = (('M', "Male"), ('F', "Female"), ('U', "Unspecified"))
    gender_type = models.CharField(default='F', choices=gender_type_data, max_length=10)
    approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    specialization = models.CharField(max_length=25)
    about= models.CharField(max_length=1000)
    def __str__(self):
        return f'{self.user}'


@receiver(post_save, sender=CustomUser)
# Now Creating a Function which will automatically insert data in HOD, Staff or Student
def create_user_profile(sender, instance, created, **kwargs):
    # if Created is true (Means Data Inserted)
    if created:
        # Check the user_type and insert the data in respective tables
        if instance.user_type == 'P':
            Patient.objects.create(user=instance, address="", profile_pic="", phone_number=0, dob='1990-12-1', gender_type="M")
        if instance.user_type == 'D':
            Doctor.objects.create(user=instance,address="", profile_pic="", phone_number=0, dob='1999-12-10', gender_type="M",approved=False,
                                  specialization="", about="")


@receiver(post_save, sender=CustomUser)
def save_user_profile(sender, instance, **kwargs):
    if instance.user_type == 'P':
        instance.patient.save()
    if instance.user_type == 'D':
        instance.doctor.save()