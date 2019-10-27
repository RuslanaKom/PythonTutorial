from django.core.mail import EmailMessage


subject = 'Message from Python 2'
text = 'Hsssss-sss  ssss ss'
addressFrom = 'stuffost@gmail.com'
addressesTo = ['stuffost@gmail.com']

email = EmailMessage(
subject,
text,
addressFrom,
addressesTo,
[],
reply_to=[],
headers={'Message-ID': 'foo'},
)

email.send(fail_silently=False)