from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ObjectDoesNotExist


class QuestionQuerySet(models.QuerySet):
    def new(self):
        return self.order_by('-time_created')

    def hot(self):
        return self.order_by('-rating')

    def questions_by_tag(self, tag: str):
        return self.filter(tags__name=tag)


class QuestionManager(models.Manager):
    def get_queryset(self):
        return QuestionQuerySet(model=self.model, using=self._db)
    
    def get_by_id(self, id: int):
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

    def questions_by_tag(self, tag: str):
        try:
            questions = self.get_queryset().questions_by_tag(tag)
        except ObjectDoesNotExist:
            return None
        return questions


class TagManager(models.Manager):
    def best_tags(self):
        return self.all().order_by('-rating')
    
    def create_or_get_tag(self, tag: str):
        tag = ''.join(tag.split())
        try:
            tag_obj = self.get(name=tag)
        except ObjectDoesNotExist:
            tag_obj = self.create(name=tag)
        return tag_obj


class UserQuerySet(models.QuerySet):   
    def user_by_username(self, username: str):
        return self.get(user__username=username)

    def validate_user(self, username, password):
        return self.get(user__username=username, user__password=password)
        


class UserManager(models.Manager):
    def get_queryset(self):
        return UserQuerySet(model=self.model, using=self._db)

    def user_by_username(self, username: str):
        try:
            user = self.get_queryset().user_by_username(username)
        except ObjectDoesNotExist:
            return None
        return user
    
    def validate_user(self, username, password: str):
        try:
            user = self.get_queryset().validate_user(username, password)
        except ObjectDoesNotExist:
            return None
        return user

    # def count_rating(self):
    #     rating = self.reactions__positive.filter(positive = True)
    #     rating -= self.reactions__positive.filter(positive = False)
    #     return rating


# class ReactionManager(models.Manager):
#     def add_reaction(self, obj, user, reaction_type):
#         obj_type = ContentType.objects.get_for_model(obj)
#         reaction = self.create(content_type=obj_type, object_id=obj.id, user=user, positive=reaction_type)
#         return reaction

#     def voted(self, obj, user) -> bool:
#         obj_type = ContentType.objects.get_for_model(obj)
#         reactions = self.filter(content_type=obj_type, object_id=obj.id, user=user)
#         return reactions.exists()