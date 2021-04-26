
from django.contrib import admin
from .models import Ticket, Feedback, FeedBackImage
from authentication.models import User


class OwnerTabularInline(admin.TabularInline):
    model = User


class FeedbackTabularInline(admin.TabularInline):
    model = Feedback
    extra = 1
    classes = ('collapse',)


class TicketTabularInline(admin.TabularInline):
    model = Ticket


class FeedbackImageTabularInline(admin.TabularInline):
    model = FeedBackImage
    classes = ('collapse',)
    extra = 1


class TicketAdmin(admin.ModelAdmin):
    inlines = [FeedbackTabularInline]

    list_display = ('first_name', 'last_name',
                    'appointment_date', 'service_type', 'created_at', 'feedback_count')

    list_display_links = ('first_name', 'last_name',)

    list_filter = ('terms_approved', 'service_type', 'is_intake_call',
                   'appointment_date', 'created_at')
    empty_value_display = 'unknown'
    search_fields = ['first_name', 'last_name',
                     'email', 'owner__zip_address', 'owner__address']

    raw_id_fields = ('owner', )


class FeedbackAdmin(admin.ModelAdmin):
    inlines = [FeedbackImageTabularInline]

    list_display = ('owner_id', 'ticket_id', 'created_at', )

    list_display_links = ('owner_id', 'ticket_id',)

    #list_filter = ('created_at', "owner", "ticket")

    empty_value_display = 'unknown'
    search_fields = ['owner__first_name', 'owner__last_name',
                     'owner__email', 'owner__zip_address', 'owner__address']

    raw_id_fields = ('owner', 'ticket')


admin.site.register(Ticket, TicketAdmin)

admin.site.register(Feedback, FeedbackAdmin)
admin.site.register(FeedBackImage)
