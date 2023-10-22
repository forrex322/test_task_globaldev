from datetime import datetime, timedelta

from django.db.models import Sum, Q

from booktimetracker.models import ReadingSession
from taskapp.celery import app
from users.models import User


@app.task
def collect_reading_time_statistic():
    """
    Async task that collects information about reading sessions by last 7 and 30 days.
    """
    users = User.objects.all()

    for user in users:
        total_time = ReadingSession.objects.filter(user=user,).aggregate(
            total_time_by_7_days=Sum(
                "duration_of_session",
                filter=Q(start_reading_session__gte=datetime.now() - timedelta(days=7)),
            ),
            total_time_by_30_days=Sum(
                "duration_of_session",
                filter=Q(
                    start_reading_session__gte=datetime.now() - timedelta(days=30)
                ),
            ),
        )
        user.profile.last_7_days_statistic = total_time["total_time_by_7_days"]
        user.profile.last_30_days_statistic = total_time["total_time_by_30_days"]
        user.profile.save()
