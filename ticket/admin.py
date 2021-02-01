from django.contrib import admin
from .models import Ticket, Feedback, FeedBackImage
admin.site.register(Ticket)
admin.site.register(Feedback)
admin.site.register(FeedBackImage)
