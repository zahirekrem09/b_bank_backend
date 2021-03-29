from datetime import date
from django.db.models.query import QuerySet
from apscheduler.schedulers.background import BackgroundScheduler
from rest_framework import serializers
from ticket.models import Ticket
from authentication.models import User
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags


def sent_mail():
    from datetime import date, timedelta, time, datetime
    from django.utils import timezone
    today = timezone.now()
    print(today)
    tomorrow = today + timedelta(days=1)

    qs = Ticket.objects.filter(appointment_date__year=tomorrow.year,
                               appointment_date__month=tomorrow.month, appointment_date__day=tomorrow.day)
    for q in qs:

        try:
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
        except:
            pass

    # print(qs)


def start():
    scheduler = BackgroundScheduler()
    scheduler.add_job(sent_mail, 'interval',
                      minutes=1200, id="send_mail_001", replace_existing=True)
    scheduler.start()


# today = date.today()

# timeit[Model.objects.filter(date_created__year=today.year,
#                             date_created__month=today.month, date_created__day=today.day)]
# 1000 loops, best of 3: 652 us per loop

# timeit[Model.objects.filter(date_created__gte=today)]
# 1000 loops, best of 3: 631 us per loop

# timeit[Model.objects.filter(date_created__startswith=today)]
# 1000 loops, best of 3: 541 us per loop

# timeit[Model.objects.filter(date_created__contains=today)]
# 1000 loops, best of 3: 536 us per loop


# today = date.today()
# today_filter = MyModel.objects.filter(post_date__year=today.year,
#                                       post_date__month=today.month,
#                                       post_date__day=today.day)
