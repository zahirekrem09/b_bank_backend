from django.contrib import admin
from django.contrib.auth.models import Group
from .models import User, ServiceType


class UserAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email',
                    'is_pro', 'is_client', 'is_connector', 'is_sponsor', 'created_at')

    list_display_links = ('first_name', 'last_name', 'email',)

    list_filter = ('is_pro', 'is_client', 'is_connector',
                   'is_sponsor', 'created_at')
    empty_value_display = 'unknown'
    search_fields = ['first_name', 'last_name',
                     'email', 'company_name', 'zip_address', 'address']


admin.site.register(User, UserAdmin)
admin.site.register(ServiceType)
admin.site.unregister(Group)

# Register your models here.


# class AuthorAdmin(admin.ModelAdmin):
#     fields = ('name', 'title', 'view_birth_date')

#     def view_birth_date(self, obj):
#         return obj.birth_date

#     view_birth_date.empty_value_display = '???'
# list_filter = ('company__name',)
