from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
from django.templatetags.static import static
from django.utils.html import mark_safe


from PIL import Image
from shortuuid.django_fields import ShortUUIDField



RELATIONSHIP = (
    ("single","Single"),
    ("married","married"),
    ("inlove","In Love"),
)


GENDER = (
    ("female", "Female"),
    ("male", "Male"),
)

WHO_CAN_SEE_MY_FRIENDS = (
    ("Only Me","Only Me"),
    ("Everyone","Everyone"),
)


def user_directory_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = "%s.%s" % (instance.user.id, ext)
    return 'user_{0}/{1}'.format(instance.user.id,  filename)


class MyAccountManager(BaseUserManager):
    def create_user(self, first_name, last_name, username, email, password=None):
        if not email:
            raise ValueError("Users must have an email address")

        user = self.model(
            email=self.normalize_email(email),
            username=username,
            first_name=first_name,
            last_name=last_name,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, first_name, last_name, username, email, password):

        user = self.create_user(
            email=self.normalize_email(email),
            username=username,
            password=password,
            first_name=first_name,
            last_name=last_name,
        )
        user.is_admin = True
        user.is_active = True
        user.is_staff = True
        user.is_superuser = True
        user.is_superadmin = True

        user.save(using=self._db)
        return user


class Account(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(max_length=100, unique=True)
    phone_number = models.CharField(max_length=50)

    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now_add=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_superadmin = models.BooleanField(default=False)

    objects = MyAccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, add_label):
        return True



class Profile(models.Model):
    pid = ShortUUIDField(length=7, max_length=25, alphabet="abcdefghijklmnopqrstuvxyz123")
    user = models.OneToOneField(Account, on_delete=models.CASCADE)
    cover_image = models.ImageField(upload_to=user_directory_path, blank=True, null=True)
    image = models.ImageField(upload_to=user_directory_path, blank=True, null=True)
    full_name = models.CharField(max_length=1000, null=True, blank=True)
    bio = models.CharField(max_length=100, null=True, blank=True)
    about_me = models.CharField( max_length=1000,null=True, blank=True)
    phone = models.CharField(max_length=100, null=True, blank=True)
    gender = models.CharField(max_length=100, choices=GENDER, null=True, blank=True)
    relationship = models.CharField(max_length=100, choices=RELATIONSHIP, null=True, blank=True, default="single")
    friends_visibility = models.CharField(max_length=100, choices=WHO_CAN_SEE_MY_FRIENDS, null=True, blank=True, default="Everyone")
    country = models.CharField(max_length=100, null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    state = models.CharField(max_length=100, null=True, blank=True)
    address = models.CharField(max_length=1000, null=True, blank=True)
    working_at = models.CharField(max_length=1000, null=True, blank=True)
    verified = models.BooleanField(default=False)
    followers = models.ManyToManyField(Account, blank=True, related_name="followers")
    followings = models.ManyToManyField(Account, blank=True, related_name="followings")
    friends = models.ManyToManyField(Account, blank=True, related_name="friends")
    blocked = models.ManyToManyField(Account, blank=True, related_name="blocked")
    date = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    class Meta:
        ordering = ["-date"]

    def __str__(self):
        if self.full_name:
            return str(self.full_name)
        else:
            return str(self.user.username)

    
    def thumbnail(self):
        return mark_safe('<img src="/media/%s" width="50" height="50" object-fit:"cover" style="border-radius: 30px;" />' % (self.image))