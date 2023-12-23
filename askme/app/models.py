from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType

from app.managers import QuestionManager, TagManager, ProfileManager


class Question(models.Model):
    title = models.CharField(max_length=30)
    content = models.TextField()
    time_created = models.DateTimeField(auto_now=False, auto_now_add=True)
    rating = models.IntegerField(default=0)

    author = models.ForeignKey('Profile', on_delete=models.PROTECT, related_name='question')
    tags = models.ManyToManyField('Tag', related_name='question')
    reactions = GenericRelation('Reaction', related_name='question')

    objects = QuestionManager()

    class Meta:
        ordering = ['-time_created']

    def __str__(self) -> str:
        return self.title
        

class Answer(models.Model):
    content = models.TextField()
    time_created = models.DateTimeField(auto_now = False, auto_now_add = True)
    correct = models.BooleanField(default=False)
    rating = models.IntegerField(default=0)

    author = models.ForeignKey('Profile', on_delete=models.PROTECT, related_name='answer')
    question = models.ForeignKey('Question', on_delete=models.CASCADE, related_name='answer')
    reactions = GenericRelation('Reaction', related_name='answer')

    # TODO: objects = Answermanager()

    class Meta:
        ordering = ['-rating']


class Tag(models.Model):
    name = models.CharField(max_length = 20)
    models.UniqueConstraint(name, 'name', name='Unique tag name')

    objects = TagManager()

    def __str__(self) -> str:
        return self.name


class Profile(models.Model):
    profile_pic = models.ImageField(blank=True, null=True, default='default-avatar.png', upload_to='avatar/%Y/%m/%d')
    rating = models.IntegerField(default=0)
    question_count = models.IntegerField(default=0)
    answer_count = models.IntegerField(default=0)
    correct_count = models.IntegerField(default=0)

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')

    objects = ProfileManager()

    def __str__(self) -> str:
        return self.user.username


class Reaction(models.Model):
    positive = models.BooleanField()
    time_created = models.DateTimeField(auto_now=False, auto_now_add=True)

    author = models.ForeignKey('Profile', on_delete=models.DO_NOTHING, related_name='reaction')

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.IntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    # TODO objects = ReactionManager()

    def __str__(self) -> str:
        return str(self.positive)