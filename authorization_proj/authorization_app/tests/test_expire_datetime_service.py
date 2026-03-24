from datetime import datetime

from django.conf import settings
from django.test import SimpleTestCase
from django.utils import timezone

from draftapp.services.expire_datetime_service import ExpireDatetimeService

# Create your tests here.


class TestExpireDatetimeService(SimpleTestCase):
    def setUp(self) -> None:
        self.past_datetime: datetime = datetime(
            1990, 1, 1, tzinfo=settings.CURRENT_TIMEZONE)
        self.future_datetime: datetime = datetime(
            2050, 12, 30, tzinfo=settings.CURRENT_TIMEZONE)
        # self.expire_datetime_service: ExpireDatetimeService = ExpireDatetimeService()

    def test_is_expare_at_valid(self) -> None:
        self.assertFalse(
            ExpireDatetimeService.is_expare_date_valid(self.past_datetime))
        self.assertTrue(
            ExpireDatetimeService.is_expare_date_valid(self.future_datetime))

    def test_get_new_expire_date(self) -> None:
        token_age = 3600
        expire_datetime_service: ExpireDatetimeService = ExpireDatetimeService(
            token_age
        )

        time_before_expire_at = datetime.fromtimestamp(
            timezone.now().timestamp() + token_age - 100,
            settings.CURRENT_TIMEZONE
        )
        time_after_expire_at = datetime.fromtimestamp(
            timezone.now().timestamp() + token_age + 200,
            settings.CURRENT_TIMEZONE
        )
        expire_at = expire_datetime_service.get_new_expire_at()

        self.assertTrue(expire_at > time_before_expire_at)
        self.assertTrue(expire_at < time_after_expire_at)
