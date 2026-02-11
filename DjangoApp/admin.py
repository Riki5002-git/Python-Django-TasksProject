from django.contrib import admin

from DjangoApp.models import Task, User, Team

# Register your models here.
admin.site.register(Task)
admin.site.register(User)
admin.site.register(Team)