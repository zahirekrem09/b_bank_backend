from django.apps import AppConfig


class AuthenticationConfig(AppConfig):
    name = 'authentication'

    def ready(self):
        print("Starting Scheduler ...")
        from ticket.send_mail_scheduler import send_mail
        send_mail.start()
