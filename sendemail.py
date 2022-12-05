import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, Bcc, Personalization, To
from urllib.error import HTTPError

def send_email(to, clubname, content):

    message = Mail(
        # display sender as the club name instead of "Katie Baldwin"
        from_email=('clubhub-admin@princeton.edu', clubname),
        subject = 'Announcement from %s' % clubname,
        html_content=content)

    personalization = Personalization()

    # personalization objects must have to field set
    personalization.add_to(To('clubhub-admin@princeton.edu'))

    # add all of the emails as Bcc fields
    for email in to:
        personalization.add_bcc(Bcc(email))

    message.add_personalization(personalization)

    try:
        sendgrid_client = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
        response = sendgrid_client.send(message)
        print(response.status_code)
        print(response.body)
        print(response.headers)

    except Exception as e:
        print("Error:", e.to_dict)
        return "error, send_email"

    return "success"


def append_address(subscribers):

    emails = []
    for each in subscribers:
        emails.append(each+"@princeton.edu")

    return emails
