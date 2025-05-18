import base64
import random
import string

from django.conf import settings
from django.core.mail import send_mail


def confirmation_code_generator(size=8, chars=string.digits):
    return ''.join(random.choice(chars) for x in range(size))

def encode_email(email: str): 
    return base64.b64encode(email.encode('utf-8')).decode('utf-8')

def decode_email(encoded_email):
    return base64.b64decode(encoded_email.encode('utf-8')).decode('utf-8')



def send_verification_code_to_email(email: str): 
    code = confirmation_code_generator()
    send_mail('Activation code', 
              f"Your activation code is: {code}\n\nno-reply@gmail.com", 
              settings.EMAIL_HOST_USER, [email])
    return code


def send_verification_code_to_email_to_change_email(email: str):
    code = confirmation_code_generator()
    send_mail('Confirmation code to change email', f'Your verification password is: {code}\n', 
              settings.EMAIL_HOST_USER, [email])
    return code


def send_verification_code_to_email__second_version(email: str):
    code = confirmation_code_generator()
    subject = "Thank you for signing up for Fasttracks!"
    html_message = f"""<html> 
                        <body>
                            <h4>We`re excited to see your selfies!</h4>
                            <h4>To complete your registration, please enter the code to previous site</h4>
                            <h4>Your Activation code is: {code}</h4>
                        </body>
                        </html>"""
    send_mail(subject=subject, html_message=html_message, message='', from_email=settings.EMAIL_HOST_USER, recipient_list=[email])
    return code
