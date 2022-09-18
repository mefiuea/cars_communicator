from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MaxLengthValidator, RegexValidator
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin


# Validators
phone_regex = RegexValidator(
    regex=r'(?<!\w)(\(?(\+|00)?48\)?)?[ -]?\d{3}[ -]?\d{3}[ -]?\d{3}(?!\w)')


class Messages(models.Model):
    creator = models.ForeignKey(
        get_user_model(), related_name='message_creator', on_delete=models.PROTECT)
    creation_date = models.DateField(auto_now_add=True)
    creation_time = models.TimeField(auto_now_add=True)
    content = models.TextField(blank=False, validators=[
                               MaxLengthValidator(700)])
    thread = models.ForeignKey(
        'Thread', related_name='messages_thread', on_delete=models.PROTECT)

    def __str__(self):
        return f'Message {self.thread}, creator: {self.creator}'


class Thread(models.Model):
    creator = models.ForeignKey(
        get_user_model(), related_name='thread_creator', on_delete=models.PROTECT)
    subject = models.CharField(
        max_length=50, unique=False, blank=True, default='')
    creation_date = models.DateField(auto_now_add=True)
    creation_time = models.TimeField(auto_now_add=True)
    second_person = models.ForeignKey(
        get_user_model(), related_name='thread_second_person', on_delete=models.PROTECT)
    messages = models.ManyToManyField(
        'Messages', related_name='thread_messages', blank=True)

    def __str__(self):
        return self.subject


class RegisteredCars(models.Model):
    brand = models.CharField(max_length=50, unique=False, blank=False)
    model = models.CharField(max_length=50, unique=False, blank=False)
    registration_date = models.DateField(auto_now_add=True)
    registration_time = models.TimeField(auto_now_add=True)
    owners = models.ManyToManyField(
        get_user_model(), related_name='registeredcars_creator')
    registration_number = models.CharField(
        max_length=10, unique=True, blank=False)

    def __str__(self):
        return f'Registered car: {self.registration_number}'


class MyUserManager(BaseUserManager):
    def create_user(self, email, user_name, password=None):
        if not email:
            raise ValueError('User must provide email.')
        if not user_name:
            raise ValueError('User must provide user name.')

        user = self.model(
            email=self.normalize_email(email),
            user_name=user_name,
        )

        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, user_name, password=None):
        user = self.create_user(
            email=self.normalize_email(email),
            user_name=user_name,
            password=password
        )
        user.is_admin = True
        user.is_staff = True
        user.is_active = True
        user.is_superuser = True
        user.is_email_verified = True
        user.save(using=self._db)

        return user


class MyUser(AbstractBaseUser, PermissionsMixin):
    user_name = models.CharField(
        max_length=30, unique=False, verbose_name='user name')
    first_name = models.CharField(
        max_length=30, unique=False, verbose_name='first name')
    last_name = models.CharField(
        max_length=30, unique=False, verbose_name='last name')
    email = models.EmailField(
        max_length=100, unique=True, verbose_name='email')
    phone_number = models.CharField(
        max_length=17, unique=True, blank=False, validators=[phone_regex])
    cars = models.ManyToManyField(
        'RegisteredCars', related_name='user_registeredcars')
    is_email_verified = models.BooleanField(default=False)
    date_joined = models.DateTimeField(
        verbose_name='date joined', auto_now_add=True)
    last_login = models.DateTimeField(verbose_name='last login', auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    # REQUIRED_FIELDS = ['user_name', ]

    objects = MyUserManager()

    def __str__(self):
        return self.email
