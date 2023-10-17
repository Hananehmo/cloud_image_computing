import requests

API_KEY = 'd53311ba8fbcdc327bad1bf9985ed1bd-3750a53b-2c72dbc9'
DOMAIN = 'sandbox98ea0204ae724208a828fb96b1060796.mailgun.org'


def send_email(to, text):
    url = f'https://api.mailgun.net/v3/{DOMAIN}/messages'
    auth = ('api', API_KEY)
    data = {
        'from': 'Your Name <hnnemntzr200@gmail.com>',
        'to': to,
        'subject': 'Your Status',
        'text': text
    }
    response = requests.post(url, auth=auth, data=data)
    if response.status_code == 200:
        print('Email sent successfully!')
        print('Email sent:', response.json())
    else:
        print('Failed to send email. Status code:', response.status_code)
        print('Error sending email:', response.json())


send_email('recipient@example.com', 'This is the email content.')
