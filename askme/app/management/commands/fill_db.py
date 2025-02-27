from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from faker import Faker
import random

from app.models import Question, Answer, Tag, Profile, Reaction


class Command(BaseCommand):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.faker = Faker()


    def add_arguments(self, parser):
        parser.add_argument('ratio', type=int, default=10)


    def handle(self, *args, **options):
        ratio = int(options['ratio'])

        self.create_users(ratio)
        prof_min_id = Profile.objects.order_by('id')[0].id
        prof_max_id = Profile.objects.order_by('-id')[0].id
        self.create_tags(ratio)
        tag_min_id = Tag.objects.order_by('id')[0].id
        tag_max_id = Tag.objects.order_by('-id')[0].id
        self.create_questions(ratio * 10, prof_min_id, prof_max_id, tag_min_id, tag_max_id)
        que_min_id = Question.objects.order_by('id')[0].id
        que_max_id = Question.objects.order_by('-id')[0].id
        self.create_answers(ratio * 100, prof_min_id, prof_max_id, que_min_id, que_max_id)
        ans_min_id = Answer.objects.order_by('id')[0].id
        ans_max_id = Answer.objects.order_by('-id')[0].id
        self.create_reactions(ratio, prof_min_id, prof_max_id, que_min_id, que_max_id, ans_min_id, ans_max_id)
        print("Success!")


    def create_users(self, count):
        print("Creating users...")
        users = []
        profiles = []
        for i in range(count):
            users.append(User.objects.create(username=self.faker.unique.user_name(), first_name=self.faker.first_name(), last_name=self.faker.last_name(), email=self.faker.email(), password=self.faker.password()))
            profiles.append(Profile(user=users[i], profile_pic="../../../static/img/default-avatar.png"))
        profiles = Profile.objects.bulk_create(profiles)


    def create_tags(self, count):
        print("Creating tags ...")
        tags = []
        for i in range(count):
            tags.append(Tag(name=self.faker.word()))
        tags = Tag.objects.bulk_create(tags)


    def create_questions(self, count, prof_min_id, prof_max_id, tag_min_id, tag_max_id):
        print("Creating questions ...")
        questions = []
        for i in range(count):
            title = self.faker.word() + '?'
            content = self.faker.word()
            profile_id = random.randint(prof_min_id, prof_max_id)
            questions.append(Question(content=content, title=title, author_id=profile_id))
        questions = Question.objects.bulk_create(questions)
        tags = [None] * 5 
        for i in range(count):
            n_tags = random.randint(1, 5)
            for j in range(n_tags):
                tags[j] = Tag.objects.get(id=random.randint(tag_min_id, tag_max_id))
            question = Question.objects.get(pk=(i + 1))
            question.tags.add(*tags[:n_tags])
            question.save()


    def create_answers(self, count, prof_min_id, prof_max_id, que_min_id, que_max_id):
        print("Creating answers ...")
        answers = []
        for i in range(count):
            content = self.faker.word()
            profile_id = random.randint(prof_min_id, prof_max_id)
            question_id = random.randint(que_min_id, que_max_id)
            answers.append(Answer(content=content, author_id=profile_id, question_id=question_id))
        answers = Answer.objects.bulk_create(answers)


    def create_reactions(self, count, prof_min_id, prof_max_id, que_min_id, que_max_id, ans_min_id, ans_max_id):
        print("Creating reactions ...")
        question_reactions = []
        for i in range(count * 100):
            profile_id = random.randint(prof_min_id, prof_max_id)
            question_id = random.randint(que_min_id, que_max_id)
            question = Question.objects.get(id=question_id)
            delta = bool(random.randint(0, 1))
            question.rating += random.randint(-100, 100)
            question.save()
            question_reactions.append(Reaction(author_id=profile_id, content_object=question, positive=delta))
        question_reactions = Reaction.objects.bulk_create(question_reactions)

        answer_reactions = []
        for i in range(count * 100):
            profile_id = random.randint(prof_min_id, prof_max_id)
            answer_id = random.randint(ans_min_id, ans_max_id)
            answer = Answer.objects.get(id=answer_id)
            delta = bool(random.randint(0, 1))
            answer.rating += random.randint(-10, 10)
            answer.save()
            answer_reactions.append(Reaction(author_id=profile_id, content_object=answer, positive=delta))
        answer_reactions = Reaction.objects.bulk_create(answer_reactions)