from django.contrib import admin
from .models import Student, Teacher, Course, Attendance, Result


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ("name", "student_id", "email", "phone", "course")
    search_fields = ("name", "student_id", "email")


@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ("name", "teacher_id", "email", "phone")
    search_fields = ("name", "teacher_id", "email")


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ("name", "code", "teacher")
    search_fields = ("name", "code")


@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ("student", "course", "date", "present")
    list_filter = ("present", "date")


@admin.register(Result)
class ResultAdmin(admin.ModelAdmin):
    list_display = ("student", "course", "marks", "grade")
    search_fields = ("student__name", "course__name")