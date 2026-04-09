from django.contrib import admin
from .models import User, Subject, Topic, ExamSchedule, Result


admin.site.register(Subject)
admin.site.register(Topic)
admin.site.register(ExamSchedule)
admin.site.register(Result)
admin.site.register(User)
