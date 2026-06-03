from django.db import models
from django.db.models import Avg, Case, When, Value, FloatField


class Faculty(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    @property
    def total_departments(self):
        return Department.objects.filter(faculty=self).count()

    @property
    def total_feedbacks(self):
        return FeedBack.objects.filter(department__faculty=self).count()

    @property
    def rating(self):
        result = (
            FeedBack.objects.filter(department__faculty=self)
            .annotate(
                ball=Case(
                    When(status="bad", then=Value(2.0)),  # Yomon -> 2 ball
                    When(status="good", then=Value(3.5)),  # O'rtacha -> 3.5 ball
                    When(status="best", then=Value(5.0)),  # Yaxshi -> 5.0 ball
                    default=Value(0.0),
                    output_field=FloatField(),
                )
            )
            .aggregate(avg_rating=Avg("ball"))
        )

        return round(result["avg_rating"], 1) if result["avg_rating"] else 0.0


class Department(models.Model):
    name = models.CharField(max_length=100)
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    @property
    def total_feedbacks(self):
        return FeedBack.objects.filter(department=self).count()

    @property
    def last_feedback(self):
        feed = self.feedback_set.order_by("-created").first()
        return feed.created if feed else None

    @property
    def rating(self):
        result = (
            FeedBack.objects.filter(department=self)
            .annotate(
                ball=Case(
                    When(status="bad", then=Value(2.0)),  # Yomon -> 2 ball
                    When(status="good", then=Value(3.5)),  # O'rtacha -> 3.5 ball
                    When(status="best", then=Value(5.0)),  # Yaxshi -> 5.0 ball
                    default=Value(0.0),
                    output_field=FloatField(),
                )
            )
            .aggregate(avg_rating=Avg("ball"))
        )

        return round(result["avg_rating"], 1) if result["avg_rating"] else 0.0


class FeedBack(models.Model):
    class STATUS(models.TextChoices):
        BAD = "bad", "Yomon"
        GOOD = "good", "Yaxshi"
        BEST = "best", "A'lo"

    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    description = models.TextField()
    status = models.CharField(max_length=100, choices=STATUS)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.status
