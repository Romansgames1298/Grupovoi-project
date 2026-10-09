import calendar

from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import Group
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from .forms import EventForm, ForumMessageForm, ForumTopicForm, ProfileForm, RegisterForm
from .models import Event, ForumTopic, Profile


def can_manage(request):
    profile, _ = Profile.objects.get_or_create(user=request.user)
    return profile.role in ('admin', 'moderator')


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


def forum_view(request):
    topics = ForumTopic.objects.all()
    return render(request, 'forum.html', {'topics': topics})


@login_required
def topic_view(request, topic_id):
    topic = get_object_or_404(ForumTopic, id=topic_id)
    form = ForumMessageForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        message = form.save(commit=False)
        message.topic = topic
        message.author = request.user
        message.save()
        return redirect('topic', topic_id=topic.id)
    return render(request, 'topic.html', {'topic': topic, 'form': form})


@login_required
def topic_create(request):
    if not can_manage(request):
        return HttpResponseForbidden('Тільки адміністратор або модератор може створювати теми.')
    form = ForumTopicForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        topic = form.save(commit=False)
        topic.author = request.user
        topic.save()
        return redirect('forum')
    return render(request, 'topic_form.html', {'form': form, 'title': 'Нова тема'})


@login_required
def topic_edit(request, topic_id):
    if not can_manage(request):
        return HttpResponseForbidden('Недостатньо прав.')
    topic = get_object_or_404(ForumTopic, id=topic_id)
    form = ForumTopicForm(request.POST or None, instance=topic)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('topic', topic_id=topic.id)
    return render(request, 'topic_form.html', {'form': form, 'title': 'Редагування теми'})


@login_required
def topic_delete(request, topic_id):
    if not can_manage(request):
        return HttpResponseForbidden('Недостатньо прав.')
    topic = get_object_or_404(ForumTopic, id=topic_id)
    if request.method == 'POST':
        topic.delete()
        return redirect('forum')
    return render(request, 'confirm_delete.html', {'object': topic, 'kind': 'тему'})


def events_view(request):
    events = Event.objects.all()
    today = timezone.localdate()
    calendar_rows = []

    for week in calendar.monthcalendar(today.year, today.month):
        row = []
        for day in week:
            day_events = []
            if day != 0:
                day_events = events.filter(
                    date__year=today.year,
                    date__month=today.month,
                    date__day=day,
                )
            row.append({'number': day, 'events': day_events})
        calendar_rows.append(row)

    return render(request, 'events.html', {
        'events': events,
        'calendar_rows': calendar_rows,
        'month_name': today.strftime('%B %Y'),
    })


@login_required
def event_create(request):
    if not can_manage(request):
        return HttpResponseForbidden('Тільки адміністратор або модератор може керувати подіями.')
    form = EventForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        event = form.save(commit=False)
        event.author = request.user
        event.save()
        return redirect('events')
    return render(request, 'event_form.html', {'form': form, 'title': 'Нова подія'})


@login_required
def event_edit(request, event_id):
    if not can_manage(request):
        return HttpResponseForbidden('Недостатньо прав.')
    event = get_object_or_404(Event, id=event_id)
    form = EventForm(request.POST or None, instance=event)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('events')
    return render(request, 'event_form.html', {'form': form, 'title': 'Редагування події'})


@login_required
def event_delete(request, event_id):
    if not can_manage(request):
        return HttpResponseForbidden('Недостатньо прав.')
    event = get_object_or_404(Event, id=event_id)
    if request.method == 'POST':
        event.delete()
        return redirect('events')
    return render(request, 'confirm_delete.html', {'object': event, 'kind': 'подію'})
