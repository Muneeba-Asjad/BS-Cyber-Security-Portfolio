from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from .models import Student, Teacher, Course, Attendance, Result


def login_view(request):
    if request.user.is_authenticated:
        return redirect("dashboard")

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:
            login(request, user)
            return redirect("dashboard")

        return render(
            request,
            "students/login.html",
            {"error": "Invalid username or password"}
        )

    return render(request, "students/login.html")


def logout_view(request):
    logout(request)
    return redirect("login")


@login_required(login_url="/login/")
def dashboard(request):
    context = {
        "students": Student.objects.count(),
        "teachers": Teacher.objects.count(),
        "courses": Course.objects.count(),
        "attendance": Attendance.objects.count(),
        "results": Result.objects.count(),
    }

    return render(request, "students/dashboard.html", context)


@login_required(login_url="/login/")
def student_list(request):
    students = Student.objects.all()

    return render(
        request,
        "students/student_list.html",
        {"students": students}
    )


@login_required(login_url="/login/")
def teacher_list(request):
    teachers = Teacher.objects.all()

    return render(
        request,
        "students/teacher_list.html",
        {"teachers": teachers}
    )


@login_required(login_url="/login/")
def course_list(request):
    courses = Course.objects.all()

    return render(
        request,
        "students/course_list.html",
        {"courses": courses}
    )


@login_required(login_url="/login/")
def attendance_list(request):
    attendance = Attendance.objects.select_related(
        "student",
        "course"
    ).all()

    return render(
        request,
        "students/attendance_list.html",
        {"attendance": attendance}
    )


@login_required(login_url="/login/")
def result_list(request):
    results = Result.objects.select_related(
        "student",
        "course"
    ).all()

    return render(
        request,
        "students/result_list.html",
        {"results": results}
    )