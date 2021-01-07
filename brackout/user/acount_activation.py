from django.contrib.auth import get_user_model
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from django.core.mail import EmailMessage
from django.contrib.auth.tokens import default_token_generator


class AcountActivation:    
    """Creating an activation code for activating acounts
     and send emails"""
    
    def __init__(self, request, user):
        self.user = user
        self.request = request
        #token = TokenGenerator().make_token(user)
        token = default_token_generator.make_token(user)
        user_id_b64 = urlsafe_base64_encode(force_bytes(user.id))
        self.domain = get_current_site(request).domain
        self.link = reverse(
                    'user:user-activation',
                    kwargs={
                        'uidb64': user_id_b64,
                        'token': token
                    }
               )

    def send_email(self):
        mail_body = f'''
        Hey {self.user.name}!
        For activating your acount click on the link bellow:
        http://{self.domain}{self.link}
        Or use this code to activate your acount:
        code
        '''
        activation_email = EmailMessage(
            subject='Activate your Acount',
            body=mail_body,
            from_email='armanhadi728@gmail.com',
            to=(self.user.email,)
        )
        activation_email.send(fail_silently=False)
