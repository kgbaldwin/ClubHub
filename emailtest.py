# using SendGrid's Python Library
# https://github.com/sendgrid/sendgrid-python

import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

message = Mail(
    from_email='kgb2@princeton.edu',
    to_emails='pnaphade@princeton.edu',
    subject='HELLO :D',
    html_content='Another hi hi hi clubhub team!!')
try:
    sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
    response = sg.send(message)
    print("Response status code:")
    print(response.status_code)
    print("----------------------------------------")
    print("Response body:")
    print(response.body)
    print("----------------------------------------")
    print("Response headers:")
    print(response.headers)
except Exception as e:
    print(e)
