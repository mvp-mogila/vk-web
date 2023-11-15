from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType

from app.managers import QuestionManager, TagManager, UserManager


class Question(models.Model):
    title = models.CharField(max_length=50)
    content = models.TextField()
    time_created = models.DateTimeField(auto_now=False, auto_now_add=True)
    rating = models.IntegerField(default=0)

    author = models.ForeignKey("Profile", on_delete=models.PROTECT, related_name="question")
    tags = models.ManyToManyField("Tag", related_name="question")
    reactions = GenericRelation("Reaction")

    objects = QuestionManager()

    def __str__(self):
        return self.title
        

class Answer(models.Model):
    content = models.TextField()
    time_created = models.DateTimeField(auto_now = False, auto_now_add = True)
    correct = models.BooleanField(default=False)
    rating = models.IntegerField(default=0)

    author = models.ForeignKey("Profile", on_delete=models.PROTECT, related_name="answer")
    question = models.ForeignKey("Question", on_delete=models.CASCADE, related_name="answer")
    reactions = GenericRelation("Reaction")

    class Meta:
        ordering = ['rating']

    def __str__(self):
        return self.content


class Tag(models.Model):
    name = models.CharField(max_length = 50)

    objects = TagManager()

    def __str__(self):
        return self.name


class Profile(models.Model):
    profile_pic = models.ImageField(blank=True, null=True, upload_to="../uploads")
    rating = models.IntegerField(default=0)

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")

    objects = UserManager()

    def __str__(self):
        return self.user.username


class Reaction(models.Model):
    positive = models.BooleanField()
    time_created = models.DateTimeField(auto_now=False, auto_now_add=True)

    author = models.ForeignKey("Profile", on_delete=models.DO_NOTHING, related_name="reaction")

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.IntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    # objects = ReactionManager()