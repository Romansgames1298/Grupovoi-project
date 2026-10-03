from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import Group
from django.shortcuts import redirect, render

from .forms import ProfileForm, RegisterForm
from .models import Profile


def home(request):
    links = [
        {'title': 'Django Docs', 'url': 'https://docs.djangoproject.com/'},
        {'title': 'Wikipedia', 'url': 'https://uk.wikipedia.org/wiki/'},
        {'title': 'Google', 'url': 'https://www.google.com/'},
        {'title': 'GitHub', 'url': 'https://github.com/'},
    ]
    return render(request, 'home.html', {'links': links})


def register_view(request):
    form = RegisterForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        user = form.save()
        profile, _ = Profile.objects.get_or_create(
            user=user,
            defaults={'role': 'user', 'full_name': f'{user.first_name} {user.last_name}'.strip()}
        )
        if profile.role == 'user':
            group, _ = Group.objects.get_or_create(name='user')
            user.groups.add(group)
        return redirect('login')
    return render(request, 'register.html', {'form': form})


def login_view(request):
    form = AuthenticationForm(request, data=request.POST or None)
    if request.method == 'POST' and form.is_valid():
        user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
        if user is not None:
            login(request, user)
            return redirect('profile')
    return render(request, 'login.html', {'form': form})


@login_required
def profile_view(request):
    profile, _ = Profile.objects.get_or_create(user=request.user)
    form = ProfileForm(request.POST or None, instance=profile)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Дані збережено.')
        return redirect('profile')
    return render(request, 'profile.html', {'form': form, 'profile': profile})


@login_required
def dashboard_view(request):
    return render(request, 'dashboard.html', {'profile': request.user.profile})
