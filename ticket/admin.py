
from django.contrib import admin
from .models import Ticket, Feedback, FeedBackImage


class TicketAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email',
                    'appointment_date', 'service_type', 'created_at', )

    list_display_links = ('first_name', 'last_name', 'email',)

    list_filter = ('terms_approved', 'service_type', 'is_intake_call',
                   'appointment_date', 'created_at')
    empty_value_display = 'unknown'
    search_fields = ['first_name', 'last_name',
                     'email', 'owner__zip_address', 'owner__address']


admin.site.register(Ticket, TicketAdmin)

admin.site.register(Feedback)
# admin.site.register(FeedBackImage)
