from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models

class UserDetailsManager(BaseUserManager):
    def create_user(self, email, username, password=None, **extra_fields):
        if not email:
            raise ValueError("Users must have an email address")
        if not username:
            raise ValueError("Users must have a username")

        email = self.normalize_email(email)
        extra_fields.setdefault("is_active", True)
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        return self.create_user(email, username, password, **extra_fields)

class UserDetails(AbstractBaseUser):
    email = models.EmailField(unique=True, max_length=255)
    username = models.CharField(max_length=150, unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = UserDetailsManager()

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email"]

    def __str__(self):
        return self.username


# from django.db import models
# from django.contrib.auth.models import AbstractUser, Group, Permission

# class UserDetails(AbstractUser):
#     email = models.EmailField(unique=True, max_length=100)
#     #is_active = models.BooleanField(default=True)
#     date_joined = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
    
#     groups = models.ManyToManyField(Group,
#         related_name="userdetails_groups",  # Custom related_name for groups
#         blank=True
#     )
#     user_permissions = models.ManyToManyField(Permission,
#         related_name="userdetails_permissions",  # Custom related_name for permissions
#         blank=True
#     )
    
    
#     def __str__(self):
#         return self.username


# from django.db import models
# from django.contrib.auth.models import AbstractUser, BaseUserManager
# from rest_framework_simplejwt.tokens import RefreshToken

# class UserManager(BaseUserManager):
#     def create_user(self, username, email, password=None, **extra_fields):
#         if not username:
#             raise ValueError("The username field must not be empty")
#         if not email:
#             raise ValueError("The email field must not be empty.")
        
#         email = self.normalize_email(email)
#         user = self.model(username=username, email=email, **extra_fields)
#         user.set_password(password)
#         user.save(using=self._db)
#         return user
    
#     def create_superuser(self, username, email, password=None, **extra_fields):
#         extra_fields.setdefault("is_superuser", True)
#         extra_fields.setdefault("is_staff", True)
        
#         if not password:
#             raise ValueError("Password must not be empty")
        
#         return self.create_user(username, email, password, **extra_fields)
    
# class User(AbstractUser):
#     email = models.EmailField(unique=True, max_length=150)
#     is_active = models.BooleanField(default=True)
#     groups = models.ManyToManyField(
#         "auth.Group",
#         related_name = "custom_user_group",
#         blank=True,
#     )
#     user_permissions = models.ManyToManyField(
#         "auth.permission",
#         related_name="custom_user_permissions",
#         blank=True,
#     )
#     objects = UserManager()
    
#     def __str__(self):
#         return self.email
    
#     def tokens(self):
#         refresh = RefreshToken.for_user(self)
#         return {
#             'refresh': str(refresh),
#             'access': str(refresh.access_token),
#         }


# from django.contrib.auth.models import AbstractUser, Group, Permission
# from django.db import models

# class CustomUser(AbstractUser):
#     email = models.EmailField(unique=True)  # Ensure email is unique

#     # Add related_name to resolve the conflict
#     groups = models.ManyToManyField(
#         Group,
#         related_name="customuser_groups",
#         blank=True,
#         help_text="The groups this user belongs to. A user will get all permissions granted to each of their groups.",
#         verbose_name="groups",
#     )
#     user_permissions = models.ManyToManyField(
#         Permission,
#         related_name="customuser_permissions",
#         blank=True,
#         help_text="Specific permissions for this user.",
#         verbose_name="user permissions",
#     )



# from django.db import models
# from django.contrib.auth.models import User
# from django.contrib.auth.models import AbstractUser
# # # Create your models here.
# class UserDetails(AbstractUser):
    
#     phone_number = models.CharField(max_length=15, blank=True, null=True)
     
#     def __str__(self):
#         return self.username
    
    
    
    
    # user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='details')
    # email = models.EmailField()
    # password1 = models.CharField()
    # password2 = models.CharField()
    
    # def __str__(self):
    #     return f"{self.user.username}'s Details"
    
    
    


