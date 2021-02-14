from django.db.models.query import QuerySet
from rest_framework import serializers
from .models import Ticket
from authentication.models import User
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags

def sent_mail():
    from datetime import datetime, timedelta, time
    today = datetime.date.today()
    tomorrow = today + datetime.timedelta( days = 1 )
    qs = Ticket.filter(appointment_date = tomorrow )
    for q in qs:

        pro = User.objects.get(id=q.pro)
        owner = User.objects.get(id=q.owner.id)
        appointment_date = q.appointment_date
        subject, from_email = 'Ticket Detail ', 'bbankdummymail@gmail.com'
        html_content = render_to_string('ticket_detail.html', {'owner': owner, 'pro': pro, "appointment_date": appointment_date
                                                           })
        text_content = strip_tags(html_content)
        msg = EmailMultiAlternatives(subject, text_content, from_email, [
                                 pro.email, owner.email])
        msg.attach_alternative(html_content, "text/html")
        msg.send()
    print(qs)
