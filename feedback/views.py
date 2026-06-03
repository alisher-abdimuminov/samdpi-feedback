from django.http import HttpRequest
from django.shortcuts import render
from django.db.models import Avg, Case, Count, When, Value, FloatField

from .models import (
    Department,
    Faculty,
    FeedBack,
)


def landing(request: HttpRequest):
    faculties = Faculty.objects.count()
    departments = Department.objects.count()
    feedbacks = FeedBack.objects.count()

    top_departments = Department.objects.annotate(
        calculated_rating=Avg(
            Case(
                When(feedback__status="bad", then=Value(2.0)),
                When(feedback__status="good", then=Value(3.5)),
                When(feedback__status="best", then=Value(5.0)),
                default=Value(0.0),
                output_field=FloatField(),
            )
        ),
        feedbacks_count=Count("feedback"),
    ).order_by("-calculated_rating")[:5]

    context = {}
    context["top_departments"] = top_departments
    context["total_faculties"] = faculties
    context["total_departments"] = departments
    context["total_feedbacks"] = feedbacks
    return render(request=render, template_name="landing.html", context=context)


def faculties_view(request: HttpRequest):
    faculties = Faculty.objects.all()

    context = {}
    context["faculties"] = faculties
    return render(request=render, template_name="faculties.html", context=context)


def departments_view(request: HttpRequest, pk: int):
    if request.method == "POST":
        rating = request.POST.get("status", "best")
        comment = request.POST.get("description", "Zo'r")
        department = request.POST.get("department_id")
        print(department)

        department = Department.objects.filter(pk=department)

        print(rating)
        print(comment)
        print(department)

        if department:
            department = department.first()
            FeedBack.objects.create(
                department=department, description=comment, status=rating
            )

    faculty = Faculty.objects.filter(pk=pk)
    if faculty:
        faculty = faculty.first()
        departments = Department.objects.filter(faculty=faculty)
        latest_feed = (
            FeedBack.objects.filter(department__faculty=faculty)
            .order_by("-created")
            .first()
        )

        context = {}
        context["faculty"] = faculty
        context["departments"] = departments
        context["latest_feed"] = latest_feed
        return render(
            request=request, template_name="departments.html", context=context
        )
    return render(request=request, template_name="404.html")


def ratings_view(request: HttpRequest):
    departments = Department.objects.annotate(
        calculated_rating=Avg(
            Case(
                When(feedback__status="bad", then=Value(2.0)),  # Yomon -> 2 ball
                When(feedback__status="good", then=Value(3.5)),  # O'rtacha -> 3.5 ball
                When(feedback__status="best", then=Value(5.0)),  # Yaxshi -> 5.0 ball
                default=Value(0.0),
                output_field=FloatField(),
            )
        )
    ).order_by("-calculated_rating")

    faculties = Faculty.objects.all()

    search_query = request.GET.get("search")
    if search_query:
        departments = departments.filter(name__icontains=search_query)

    faculty_id = request.GET.get("faculty")
    if faculty_id:
        departments = departments.filter(faculty_id=faculty_id)

    context = {
        "departments": departments,
        "faculties": faculties,
    }
    return render(request=request, template_name="ratings.html", context=context)
