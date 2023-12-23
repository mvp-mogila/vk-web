from typing import Any
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from app.models import Answer, Question, Tag


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput) 


class RegistrationForm(UserCreationForm):
    profile_picture = forms.ImageField(required=False)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'password1', 'password2',)


class AskForm(forms.ModelForm):
    tags = forms.CharField(required=False, help_text='Enter up to 5 tags assosiated with you question divided by \',\'')    

    def clean_tags(self):
        tags = self.cleaned_data.get('tags')
        tags_list = tags.split(',')
        if (len(tags_list) > 5):
            raise forms.ValidationError('You can\'t add more than 5 tags')
        return tags_list

    class Meta:
        model = Question
        fields = ('title', 'content',)

    def save(self, author):
        new_question = Question.objects.create(author=author, title=self.cleaned_data['title'], content=self.cleaned_data['content'])
        tags_list = self.cleaned_data['tags']
        for tag in tags_list:
            question_tag = Tag.objects.create_or_get_tag(tag)
            new_question.tags.add(question_tag)
        new_question.save()
        return new_question


class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ('content',)

    def save(self, author, question):
        new_answer = Answer.objects.create(author=author, question=question, **self.cleaned_data)
        return new_answer
    

class ProfileForm(forms.ModelForm):
    profile_pic = forms.ImageField(required=False)
    
    class Meta:
        model = User
        fields = ('first_name', 'last_name',)

    def save(self, **kwargs):
        user = super().save(**kwargs)
        profile = user.profile
        if (self.cleaned_data.get('profile_pic')):
            profile.profile_pic = self.cleaned_data.get('profile_pic')
            profile.save()
        return user