from django.core.mail import send_mail

subject = 'Message from Python'
text = 'Hsssss-sss  ssss ss'
addressFrom = 'stuffost@gmail.com'
addressesTo = ['stuffost@gmail.com']

send_mail(
subject,
text,
addressFrom,
addressesTo,
fail_silently=False,
)