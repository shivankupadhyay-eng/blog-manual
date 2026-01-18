from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager

class CustomUserManager(BaseUserManager):
    def create_user(self,phone_number,password=None,**extra_fields):
        if not phone_number:
            raise ValueError("Phone number is required.")
        if not phone_number.isdigit() or len(phone_number)!=10:
            raise ValueError("Phone number should be numerical and of 10 digits.")
        
        user=self.model(
            phone_number=phone_number,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user


    def create_superuser(self,phone_number,password=None,**extra_fields):
        if not phone_number:
            raise ValueError("Phone number is required.")
        
        extra_fields.setdefault("is_staff",True)
        extra_fields.setdefault("is_superuser",True)
        extra_fields.setdefault("is_active",True)

        return self.create_user(phone_number,password=password,**extra_fields)

class CustomUser(AbstractUser):
    username=None
    is_deleted=models.BooleanField(default=False)
    phone_number=models.CharField(max_length=10,unique=True)
    profile_picture=models.ImageField(upload_to='profile_pictures',blank=True,null=True)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

    USERNAME_FIELD="phone_number"
    REQUIRED_FIELDS=[]

    objects=CustomUserManager()


class Blog(models.Model):
    title=models.CharField(max_length=100)
    picture=models.ImageField(upload_to="blogpicture/")
    description=models.TextField()
    is_deleted=models.BooleanField(default=False)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    created_by=models.ForeignKey(CustomUser,on_delete=models.CASCADE,related_name="blogs_created")
    updated_by=models.ForeignKey(CustomUser,on_delete=models.CASCADE,related_name="blogs_updated")

    class Meta:
        verbose_name="Blog"
        verbose_name_plural="Blogs"


class Comment(models.Model):
    content=models.TextField()
    blog=models.ForeignKey(Blog,on_delete=models.CASCADE,related_name="comments")
    is_deleted=models.BooleanField(default=False)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name="comments_created"
    )
    updated_by = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name="comments_updated",
        null=True,
        blank=True
    )
    class Meta:
        verbose_name="Comment"
        verbose_name_plural="Comments"


class Vote(models.Model):
    UPVOTE = 1
    DOWNVOTE = -1

    VOTE_CHOICES = (
        (UPVOTE, "Upvote"),
        (DOWNVOTE, "Downvote"),
    )

    value = models.SmallIntegerField(choices=VOTE_CHOICES)
    blog=models.ForeignKey(Blog,related_name="votes",on_delete=models.CASCADE)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name="votes_created"
    )

    class Meta:
        verbose_name="Vote"
        verbose_name_plural="Votes"
        unique_together=["blog","user"]