from django.urls import path
from . import views

urlpatterns = [
    path("", views.dashboard, name="dashboard"),

    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),

    path("students/", views.student_list, name="student_list"),
    path("teachers/", views.teacher_list, name="teacher_list"),
    path("courses/", views.course_list, name="course_list"),
    path("attendance/", views.attendance_list, name="attendance_list"),
    path("results/", views.result_list, name="result_list"),
]