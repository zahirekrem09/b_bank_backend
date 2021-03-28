from django.apps import AppConfig


class TicketConfig(AppConfig):
    name = 'ticket'

    def ready(self):
        print("Starting Scheduler ...")
        from .send_mail_scheduler import send_mail
        send_mail.start()
