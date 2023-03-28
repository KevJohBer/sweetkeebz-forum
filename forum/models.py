from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify


class Post(models.Model):
    title = models.CharField(max_length=250, unique=True)
    slug = models.SlugField(null=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='author')
    content = models.TextField(blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
    upvote = models.ManyToManyField(User, related_name='upvote', blank=True)
    downvote = models.ManyToManyField(User, related_name='downvote', blank=True)
    author_name = models.CharField(max_length=80, null=True)
    image = models.ImageField(upload_to='images/posted_pics', blank=True, default='placeholder')

    class Meta:
        ordering = ['-created_on']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("full_post", kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        return super().save(*args, **kwargs)

    def vote_result(self):
        return self.upvote.count() - self.downvote.count()


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    commenter = models.ForeignKey(User, on_delete=models.CASCADE, related_name='commenter')
    comment = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_on']


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    avatar = models.ImageField(upload_to='images/profile_pics', default='static/images/default.jpg')
    about = models.TextField(max_length=180)

    def __str__(self):
        return self.user.username


class Notification(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sender')
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='recipient')
    read = models.BooleanField(default=False)
    recieved_date = models.DateTimeField(auto_now_add=True)
