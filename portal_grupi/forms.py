from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Event, ForumMessage, ForumTopic, Profile


class RegisterForm(UserCreationForm):
    email = forms.EmailField()
    first_name = forms.CharField(max_length=50, required=False)
    last_name = forms.CharField(max_length=50, required=False)

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data.get('first_name', '')
        user.last_name = self.cleaned_data.get('last_name', '')
        if commit:
            user.save()
        return user


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('full_name', 'phone', 'bio')


class ForumTopicForm(forms.ModelForm):
    class Meta:
        model = ForumTopic
        fields = ('title', 'description')
        labels = {'title': 'Назва теми', 'description': 'Опис теми'}

    def clean_title(self):
        title = self.cleaned_data['title'].strip()
        if len(title) < 3:
            raise forms.ValidationError('Назва повинна мати хоча б 3 символи.')
        return title

    def clean_description(self):
        description = self.cleaned_data['description'].strip()
        if len(description) < 5:
            raise forms.ValidationError('Опис повинен мати хоча б 5 символів.')
        return description


class ForumMessageForm(forms.ModelForm):
    class Meta:
        model = ForumMessage
        fields = ('text',)
        labels = {'text': 'Повідомлення'}

    def clean_text(self):
        text = self.cleaned_data['text'].strip()
        if len(text) < 2:
            raise forms.ValidationError('Повідомлення занадто коротке.')
        return text


class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ('title', 'description', 'date', 'place')
        labels = {
            'title': 'Назва події',
            'description': 'Опис',
            'date': 'Дата і час',
            'place': 'Місце',
        }
        widgets = {'date': forms.DateTimeInput(attrs={'type': 'datetime-local'})}

    def clean_title(self):
        title = self.cleaned_data['title'].strip()
        if len(title) < 3:
            raise forms.ValidationError('Назва повинна мати хоча б 3 символи.')
        return title
