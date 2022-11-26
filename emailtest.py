import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

# to emails must be a list of tuples, where each tuple contains the
# recipient email address in a string (and optionally the displayed
# recipient name in a string
to_emails = [
    ('pnaphade@princeton.edu'),
    ('priyanaphade31@gmail.com'),
    ('lyoder@princeton.edu'),
    ('sejk@princeton.edu'),
    ('kgb2@princeton.edu')
]
message = Mail(
    # display sender as "The ClubHub Team" instead of "Katie Baldwin"
    from_email=('kgb2@princeton.edu', 'The ClubHub Team'),
    to_emails=to_emails,
    subject='Yet another test email',
    html_content='i <strong> love </strong> clubhub')

try:
    sendgrid_client = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
    response = sendgrid_client.send(message)
    print(response.status_code)
    print(response.body)
    print(response.headers)
except Exception as e:
    print(e)