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
        parser.add_argument('--ratio', type=int)


    def handle(self, *args, **options):
        ratio = int(options['ratio']) if options['ratio'] else 10

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
        self.create_reactions(ratio * 200, prof_min_id, prof_max_id, que_min_id, que_max_id, ans_min_id, ans_max_id)
        print("Success!")


    def create_users(self, count):
        print("Creating users...")
        users = [count]
        profiles = [count]
        for i in range(count):
            users[i] = User(username=self.faker.unique.user_name(), first_name=self.faker.first_name(), last_name=self.faker.last_name(), email=self.faker.email(), rating=random.randint(-100, 100))
            users[i].set_password(raw_password=self.faker.password())
            profiles[i] = Profile(user=users[i], avatar="../../../static/img/default-avatar.png")
        User.objects.bulk_create(users)
        Profile.objects.bulk_create(profiles)


    def create_tags(self, count):
        print("Creating tags ...")
        tags = [count]
        for i in range(count):
            tags[i] = Tag(name=self.faker.string(count=random.randint(3, 10)))

        Tag.objects.bulk_create(tags)


    def create_questions(self, count, prof_min_id, prof_max_id, tag_min_id, tag_max_id):
        print("Creating questions ...")
        questions = [count]
        for i in range(count):
            title = self.faker.string(count=random.randint(1, 20)) + '?'
            content = self.faker.word.words({count: { min: 10, max: 50 }})
            profile_id = random.randint(prof_min_id, prof_max_id)
            questions[i] = Question(content=content, title=title, profile_id=profile_id)
        questions = Question.objects.bulk_create(questions)
        tags = [5]
        for i in range(count):
            n_tags = random.randint(1, 5)
            for j in range(n_tags):
                tags[j] = Tag.objects.get(id=random.randint(tag_min_id, tag_max_id))
            questions[i].tags.add(*tags[:n_tags])
            questions[i].save()


    def create_answers(self, count, prof_min_id, prof_max_id, que_min_id, que_max_id):
        print("Creating answers ...")
        answers = [count]
        for i in range(count):
            content = self.faker.word.words({count: { min: 5, max: 30 }})
            profile_id = random.randint(prof_min_id, prof_max_id)
            question_id = random.randint(que_min_id, que_max_id)
            answers[i] = Answer(content=content, profile_id=profile_id, question_id=question_id)
        answers = Answer.objects.bulk_create(answers)


    def create_reactions(self, count, prof_min_id, prof_max_id, que_min_id, que_max_id, ans_min_id, ans_max_id):
        print("Creating reactions ...")
        question_reactions = [count // 2]
        used_pairs = []
        for i in range(count // 2):
            profile_id = random.randint(prof_min_id, prof_max_id)
            question_id = random.randint(que_min_id, que_max_id)
            while (profile_id, question_id) in used_pairs:
                profile_id = random.randint(prof_min_id, prof_max_id)
                question_id = random.randint(que_min_id, que_max_id)
            used_pairs.append((profile_id, question_id))
            question = Question.objects.get(id=question_id)
            delta = bool(random.randint(0, 1))
            if (delta):
                question.rating += 1
            else:
                question.rating -= 1
            question.save()
            question_reactions[i] = Reaction(profile_id=profile_id, content_object=question, positive=delta)
        question_reactions = Reaction.objects.bulk_create(question_reactions)

        count -= count // 2
        answer_reactions = [count]
        used_pairs = []
        for i in range(count):
            profile_id = random.randint(prof_min_id, prof_max_id)
            answer_id = random.randint(ans_min_id, ans_max_id)
            while (profile_id, answer_id) in used_pairs:
                profile_id = random.randint(prof_min_id, prof_max_id)
                answer_id = random.randint(ans_min_id, ans_max_id)
            used_pairs.append((profile_id, answer_id))
            answer = Answer.objects.get(id=answer_id)
            delta = bool(random.randint(0, 1))
            if (delta):
                answer.rating += 1
            else:
                answer.rating -= 1
            answer.save()
            answer_reactions[i] = Reaction(profile_id=profile_id, content_object=answer, positive=delta)
        answer_reactions = Reaction.objects.bulk_create(answer_reactions)