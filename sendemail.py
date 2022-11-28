import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, Bcc

def send_email(to, clubname, content):

    message = Mail(

        # display sender as the club name instead of "Katie Baldwin"
        from_email=('kgb2@princeton.edu', clubname),

        # to is a list of emails (represented as strings)
        to_emails=to,

        subject = 'Announcement from %s' % clubname,

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
        return "error, send_email"

    return "success"


def append_address(subscribers):

    emails = []
    for each in subscribers:
        emails.append(each+"@princeton.edu")

    return emails
