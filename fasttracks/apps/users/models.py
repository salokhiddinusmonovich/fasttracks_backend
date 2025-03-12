from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _


class CustomUserManager(BaseUserManager):
    def create_user(self, email: str, password: str, **extra_fields):
        if not email: raise ValueError(_("The Email must be set"))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user
    
    def create_superuser(self, email: str, password: str, **extra_fields):

        # extra_kwargs = {"is_superuser": True}
        extra_fields.setdefault("is_staff", True) # -> {"is_superuser": True, 'is_staff': True}
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:raise ValueError(_("Superuser must have is_staff=True."))
        if extra_fields.get("is_superuser") is not True:raise ValueError(_("Superuser must have is_superuser=True."))

        return self.create_user(email, password, **extra_fields)
    


class User(AbstractUser):
    
    """
    Default custom user model for fasttracks.
    If adding fields that need to be filled at user signup,
    Check forms.SignupForm as well as forms.SocialSignupForm accourdingly.
    """
    username = None
    name = models.CharField(_("Name of User"), blank=True, max_length=255)
    email = models.EmailField(_("Email address"), unique=True)
    # first_name = None -> type: ignored
    # last_name = None -> type: ignored
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
    objects = CustomUserManager()

    def is_company(self):
        from fasttracks.apps.eld.models import Company
        return Company.objects.filter(email=self.email).exists() # NOTE:  it will return true or false
    
    def __str__(self):
        return self.email
    
    def get_absolute_url(self):
        """
        Get url for user`s detail view.

        Returns:
            str: URL for user detail.
        """
        return reverse("users:detail", kwargs={"pk": self.pk})