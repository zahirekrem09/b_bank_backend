from django.contrib import admin
from django.contrib.auth.models import Group
from .models import User, ServiceType
from ticket.models import Feedback, Ticket, FeedBackImage
from rest_framework_simplejwt.token_blacklist.models import OutstandingToken, BlacklistedToken


class TicketTabularInline(admin.TabularInline):
    model = Ticket
    extra = 1
    classes = ('collapse',)


class FeedbackTabularInline(admin.TabularInline):
    model = Feedback
    extra = 1
    classes = ('collapse',)


class FeedbackImageTabularInline(admin.TabularInline):
    model = FeedBackImage


class UserAdmin(admin.ModelAdmin):
    inlines = [TicketTabularInline,
               FeedbackTabularInline]
    list_display = ('id', 'first_name', 'last_name',
                    'is_pro', 'is_client', 'is_connector', 'is_sponsor', 'created_at', 'ticket_count')

    list_display_links = ('id', 'first_name', 'last_name',)

    list_filter = ('is_pro', 'is_client', 'is_connector',
                   'is_sponsor', 'created_at', "service_type")
    empty_value_display = 'unknown'
    search_fields = ['first_name', 'last_name',
                     'email', 'company_name', 'zip_address', 'address', "service_type__name"]

    filter_horizontal = ('service_type',)


admin.site.register(User, UserAdmin)
admin.site.register(ServiceType)
admin.site.unregister(Group)
# admin.site.unregister(BlacklistedToken)
# admin.site.unregister(OutstandingToken)


# Register your models here.


# class AuthorAdmin(admin.ModelAdmin):
#     fields = ('name', 'title', 'view_birth_date')

#     def view_birth_date(self, obj):
#         return obj.birth_date

#     view_birth_date.empty_value_display = '???'
# list_filter = ('company__name',)
