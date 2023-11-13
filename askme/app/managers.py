from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ObjectDoesNotExist


class QuestionQuerySet(models.QuerySet):
    def new(self):
        return self.order_by('time_created')

    def hot(self):
        return self.order_by('-rating')


class QuestionManager(models.Manager):
    def get_queryset(self):
        return QuestionQuerySet(model=self.model, using=self._db)
    
    def get_by_id(self, id):
        try:
            question = self.get(pk=id)
        except ObjectDoesNotExist:
            return None
        return question

    def new(self):
        try:
            new_questions = self.get_queryset().new()[:100]
        except ObjectDoesNotExist:
            return None
        return new_questions
    
    def hot(self):
        try:
            hot_questions = self.get_queryset().hot()[:100]
        except ObjectDoesNotExist:
            return None
        return hot_questions


class TagManager(models.Manager):
    def questions_by_tag(self, tag_name):
        try:
            tag = self.get(name=tag_name)
        except ObjectDoesNotExist:
            return None
        questions = tag.question.all()
        return questions



# class UserManager(models.Manager):
#     def count_rating(self):
#         rating = self.reactions__positive.filter(positive = True)
#         rating -= self.reactions__positive.filter(positive = False)
#         return rating


# class ReactionManager(models.Manager):
#     def add_reaction(self, obj, user, reaction_type):
#         obj_type = ContentType.objects.get_for_model(obj)
#         reaction = self.create(content_type=obj_type, object_id=obj.id, user=user, positive=reaction_type)
#         return reaction

#     def voted(self, obj, user) -> bool:
#         obj_type = ContentType.objects.get_for_model(obj)
#         reactions = self.filter(content_type=obj_type, object_id=obj.id, user=user)
#         return reactions.exists()