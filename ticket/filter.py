from django_filters import DateRangeFilter, DateTimeFilter, DateFromToRangeFilter
from django_filters import rest_framework as djfilters
from .models import Ticket
from psycopg2.extras import DateRange
import django_filters


class DateExactRangeWidget(django_filters.widgets.DateRangeWidget):
    """Date widget to help filter by *_start and *_end."""
    suffixes = ['start', 'end']


class DateExactRangeField(django_filters.fields.DateRangeField):
    widget = DateExactRangeWidget

    def compress(self, data_list):
        if data_list:
            start_date, stop_date = data_list
            return DateRange(start_date, stop_date)


class DateExactRangeFilter(django_filters.Filter):
    """
    Filter to be used for Postgres specific Django field - DateRangeField.
    https://docs.djangoproject.com/en/2.1/ref/contrib/postgres/fields/#daterangefield
    """
    field_class = DateExactRangeField


class TicketFilter(djfilters.FilterSet):
    # created_at = DateExactRangeFilter()

    start_date = DateTimeFilter(field_name="created_at", lookup_expr=('gt'),)
    end_date = DateTimeFilter(field_name="created_at", lookup_expr=('lt'))
    date_range = DateRangeFilter(field_name="created_at",)
    created_at = DateFromToRangeFilter()

    class Meta:
        model = Ticket
        fields = ['created_at', ]
