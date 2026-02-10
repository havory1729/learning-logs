from django.contrib import admin

from .models import Entries, Topic

admin.site.register(Topic)
admin.site.register(Entries)
