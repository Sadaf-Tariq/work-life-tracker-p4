from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

from .managers import CustomUserManager


class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(_("email address"), unique=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email


class Department(models.Model):
    dept_ID = models.IntegerField(primary_key=True)
    dept_name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.dept_name


class Employee(models.Model):
    first_name = models.CharField(max_length=50, blank=False)
    last_name = models.CharField(max_length=50, blank=False)
    slug = models.SlugField(max_length=200, unique=True)
    department = models.ForeignKey(
        Department, on_delete=models.CASCADE, related_name="dept"
    )
    hired_on = models.DateTimeField(auto_now=False, auto_now_add=False)
    joined_on = models.DateTimeField(auto_now_add=True)
    work_email = models.EmailField(max_length=200, unique=True, blank=False)

    class Meta:
        ordering = ["hired_on"]

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
