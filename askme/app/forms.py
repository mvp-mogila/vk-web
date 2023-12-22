from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from app.models import Question


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput) 


class RegistrationForm(UserCreationForm):
    profile_picture = forms.ImageField(required=False)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'password1', 'password2', 'profile_picture')


class AskForm(forms.ModelForm):
    tags = forms.CharField(required=False, help_text='Enter up to 5 tags assosiated with you question divided by \',\'')    

    def clean_tags(self):
        tags = self.cleaned_data.get('tags')
        tags_list = tags.split(',')
        print(tags_list)
        if (len(tags_list) > 5):
            raise forms.ValidationError('You can\'t add more than 5 tags')
        return tags_list

    class Meta:
        model = Question
        fields = ('title', 'content', 'tags')