import pytest

from booktimetracker.tests.factories import ReadingSessionFactory
from users.tasks import collect_reading_time_statistic
from users.tests.factories import ProfileFactory

pytestmark = pytest.mark.django_db


class TestCollectUserStatistics:
    def test_collect_user_statistics_by_7_days(self, user, api_client):
        api_client.force_authenticate(user)
        profile = ProfileFactory(user=user)

        reading_session = ReadingSessionFactory(
            user=user,
            start_reading_session="2023-10-20T00:00:00Z",
            end_reading_session="2023-10-20T01:53:00Z",
            duration_of_session="01:53:00",
        )

        collect_reading_time_statistic()

        profile.refresh_from_db()
        assert str(profile.last_7_days_statistic) == "1:53:00"

    def test_collect_user_statistics_by_30_days(self, user, api_client):
        api_client.force_authenticate(user)
        profile = ProfileFactory(user=user)

        reading_session = ReadingSessionFactory(
            user=user,
            start_reading_session="2023-09-28T00:00:00Z",
            end_reading_session="2023-09-28T05:03:00Z",
            duration_of_session="05:03:00",
        )

        collect_reading_time_statistic()

        profile.refresh_from_db()
        assert str(profile.last_30_days_statistic) == "5:03:00"
