from django.contrib.sites.shortcuts import get_current_site
from rest_framework_simplejwt.tokens import RefreshToken
from decouple import config
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.core.mail import EmailMultiAlternatives


class EmailUtil:
    @staticmethod
    def send_email(request, user):

        FRONTEND_URL = config('FRONTEND_URL')

        token = RefreshToken.for_user(user).access_token
        if user.is_pro:
            userRole = "pro"
        elif user.is_client:
            userRole = "client"
        else:
            userRole = "connector"

        verify_link = FRONTEND_URL + 'email-verify/' + \
            str(token) + "?userRole=" + userRole
        subject, from_email, to = 'Verify Your Email', config(
            'EMAIL_HOST_USER'), user.email
        current_site = get_current_site(request).domain
        html_content = render_to_string('verify_email.html', {
                                        'verify_link': verify_link, 'base_url': FRONTEND_URL, 'backend_url': current_site, 'user': user})
        text_content = strip_tags(html_content)
        msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
        msg.attach_alternative(html_content, "text/html")
        msg.send()
