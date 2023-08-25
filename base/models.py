from django.db import models
from django.contrib.auth.models import AbstractUser
from cloudinary.models import CloudinaryField

class User(AbstractUser):
    name = models.CharField(max_length=100, null=True)
    username = models.CharField(unique=True, max_length=100, null=True)
    email = models.EmailField(unique=True, null=True)
    bio = models.TextField(null=True)

    # avatar = models.ImageField(
    #     upload_to='Profiles', null=True, default='avatar.jpg')
    avatar = CloudinaryField('image', default='avatar.png')
    cover_image = CloudinaryField('image', default='cover_img.jpg')
    # cover_image = models.ImageField(
    #     upload_to='CoverImages', default='cover_img.jpg', null=True)

    def __str__(self):
        return self.name


class Post(models.Model):
    host = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    # post_img = models.ImageField(upload_to='Posts')
    post_img = CloudinaryField('image')
    no_of_likes = models.IntegerField(default=0)
    caption = models.CharField(max_length=200)
    posted = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-posted']

    def __str__(self):
        return self.caption


class LikePost(models.Model):
    post_id = models.CharField(max_length=100)
    username = models.CharField(max_length=100)

    def __str__(self):
        return self.username


class Follow(models.Model):
    follower = models.CharField(max_length=100)
    user = models.CharField(max_length=100)

    def __str__(self):
        return self.follower


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    body = models.CharField(max_length=1000, null=True)
    date = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return f"{self.user}:{self.body[:20]}"
