from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models

class GuestEmail(models.Model):
    email = models.EmailField()
    active = models.BooleanField(default=True)
    update = models.DateTimeField(auto_now=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email


class CustomUserManager(BaseUserManager):

    def create_staff_user(self, email, password):
	    email = self.normalize_email(email)
	    user = self.model(email=email, password=password) #, first_name=first_name, last_name=last_name, **extra_fields)
	    user.staff = True
	    user.set_password(password)
	    user.save(using=self._db)
	    return user

    def create_user(self, email, password=None): #, first_name=None, last_name=None, **extra_fields):
        if not email:
	        raise ValueError('Enter an email address')
        # if not first_name:
	    #     raise ValueError('Enter a first name')
        # if not last_name:
	    #     raise ValueError('Enter a last name')
        email = self.normalize_email(email)
        user = self.model(email=email, password=password) #, first_name=first_name, last_name=last_name, **extra_fields)
        user.set_password(password)
        #user.set_password(self.cleaned_data["password"])
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        user = self.create_user(email, password=password)
        user.is_superuser = True
        user.admin = True
        user.staff = True
        user.save(using=self._db)
        return user


class CustomUser(AbstractUser):
	email = models.EmailField(
		verbose_name='email address',
		max_length=255,
		unique=True,
	)
	first_name = models.CharField(max_length=20)
	last_name = models.CharField(max_length=20)
	username = models.CharField(max_length=20, default=None, blank=True, null=True)
	active = models.BooleanField(default=True)
	staff = models.BooleanField(default=False)  # a admin user; non super-user
	admin = models.BooleanField(default=False)  # a superuser

	objects = CustomUserManager()

	USERNAME_FIELD = 'email'
	REQUIRED_FIELDS = []  # Email & Password are required by default.

	def get_full_name(self):
		# The user is identified by their email address
		return self.email

	def get_short_name(self):
		# The user is identified by their email address
		return self.email

	def has_perm(self, perm, obj=None):
		# Does the user have a specific permission?"
		# Simplest possible answer: Yes, always
		return True

	def has_module_perms(self, app_label):
		# Does the user have permissions to view the app `app_label`?"
		# Simplest possible answer: Yes, always
		return True

	@property
	def is_staff(self):
		return self.staff

	@property
	def is_admin(self):
		return self.admin

	@property
	def is_active(self):
		return self.active

	def __str__(self):
		return self.email
