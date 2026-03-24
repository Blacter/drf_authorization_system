from datetime import datetime

from django.conf import settings
from django.utils import timezone



class ExpireDatetimeService:
    def __init__(self):
        self._expire_datetime_utc: datetime

    def get_new_expire_date(self, token_age_sec: int) -> datetime:
        self._token_age_sec = token_age_sec
        self._calculate_expare_date()
        return self._expire_datetime_utc

    def _calculate_expare_date(self) -> None:
        self._expire_datetime_utc = datetime.fromtimestamp(
            timezone.now().timestamp() + self._token_age_sec,
            settings.CURRENT_TIMEZONE
        )

    @staticmethod
    def is_expare_date_valid(expire_date: datetime) -> bool:
        return (expire_date > timezone.now())