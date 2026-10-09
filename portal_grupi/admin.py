from django.contrib import admin

from .models import Event, ForumMessage, ForumTopic, Profile

admin.site.register(Profile)
admin.site.register(ForumTopic)
admin.site.register(ForumMessage)
admin.site.register(Event)
