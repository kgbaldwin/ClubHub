import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, Bcc

def send_email(to, clubname, content):
    # to emails must be a list of tuples, where each tuple contains the
    # recipient email address in a string (and optionally the displayed
    # recipient name in a string)

    # Convert list to list of tuples
    to_emails = []
    for email in to:
        to_emails.append((email))

    message = Mail(
        # display sender as the club name instead of "Katie Baldwin"
        from_email=('kgb2@princeton.edu', clubname),
        to_emails=to_emails,
        subject='Announcement from %s' % clubname,
        html_content=content)

    ##### figure out how to do bcc
    '''
    message.bcc = [
    Bcc('pnaphade@princeton.edu'),
    Bcc('kgb2@princeton.edu') ]
    '''

    try:
        sendgrid_client = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
        response = sendgrid_client.send(message)
        print(response.status_code)
        print(response.body)
        print(response.headers)
    except Exception as e:
        print("Error:", e)
