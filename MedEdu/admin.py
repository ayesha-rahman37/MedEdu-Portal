from django.contrib import admin
from .models import User, Subject, Topic, ExamSchedule, Result, DoctorSchedule
from .models import Book, BookIssue, BookReservation

admin.site.register(Subject)
admin.site.register(Topic)
admin.site.register(ExamSchedule)
admin.site.register(Result)
admin.site.register(User)
admin.site.register(DoctorSchedule)

# Library Models Admin
@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'isbn', 'total_copies', 'available_copies', 'category']
    list_filter = ['category', 'year']
    search_fields = ['title', 'author', 'isbn']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(BookIssue)
class BookIssueAdmin(admin.ModelAdmin):
    list_display = ['book', 'user', 'issue_date', 'due_date', 'status', 'fine_amount']
    list_filter = ['status', 'issue_date', 'due_date']
    search_fields = ['user__username', 'user__mededu_id', 'book__title']
    readonly_fields = ['issue_date', 'fine_amount']


@admin.register(BookReservation)
class BookReservationAdmin(admin.ModelAdmin):
    list_display = ['book', 'user', 'reservation_date', 'expiry_date', 'status']
    list_filter = ['status']