from django.db import models
from django.contrib.auth.models import User


class Question(models.Model):
    def __str__(self):
        return self.title

    title = models.CharField(max_length=50)
    content = models.TextField()
    date = models.DateTimeField(auto_now=False, auto_now_add=False)
    rating = models.IntegerField()

    author = models.ForeignKey("Profile", on_delete=models.PROTECT, related_name="question")
    answers = models.ForeignKey("Answer", on_delete=models.PROTECT, related_name="question")
    tags = models.ManyToManyField("Tag", related_name="question")


class Answer(models.Model):
    def __str__(self):
        return self.content

    content = models.TextField()
    date = models.DateTimeField(auto_now = False, auto_now_add = False)
    rating = models.IntegerField()
    correct = models.BooleanField()

    author = models.ForeignKey("Profile", on_delete=models.PROTECT, related_name="answer")


class Tag(models.Model):
    def __str__(self):
        return self.name

    name = models.CharField(max_length = 50)


class Profile(models.Model):
    def __str__(self):
        return self.name

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    