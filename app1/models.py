from django.db import models

# Create your models here.


class UserTypr(models.Model):
    display = models.CharField(max_length=50)

    def __str__(self):
        return self.display


class Admin(models.Model):
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=256)
    email = models.EmailField()
    user_type = models.ForeignKey('UserTypr')

    def __str__(self):
        return self.username


class Chat(models.Model):
    content = models.TextField()
    user = models.ForeignKey('Admin')
    create_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.content


class NewsType(models.Model):
    display = models.CharField(max_length=50)

    def __str__(self):
        return self.display


class News(models.Model):
    title = models.CharField(max_length=30)
    summary = models.CharField(max_length=256)
    url = models.URLField()
    favor_count = models.IntegerField(default=0)
    reply_count = models.IntegerField(default=0)
    news_type = models.ForeignKey('NewsType')
    user = models.ForeignKey('Admin')
    create_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Reply(models.Model):
    content = models.TextField()
    user = models.ForeignKey('Admin')
    new = models.ForeignKey('News')
    create_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.content
