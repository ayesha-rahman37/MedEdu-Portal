from django.contrib import admin
from .models import User, Subject, Topic, ExamSchedule, Result, DoctorSchedule, Book, Issue, ExamNotice

admin.site.register(Subject)
admin.site.register(Topic)
admin.site.register(ExamSchedule)
admin.site.register(Result)
admin.site.register(User)
admin.site.register(DoctorSchedule)
admin.site.register(Book)
admin.site.register(Issue)
admin.site.register(ExamNotice)