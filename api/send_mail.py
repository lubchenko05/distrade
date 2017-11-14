import datetime

from django.core.mail import EmailMessage


def send_order(order):
    print(order)
    msg = EmailMessage("[%s] New order!" % datetime.datetime.now(),
                       '<h3>Hello.</h3>We have new order <a href="%s">here</a><h3>Regards, Distrade.</h3>' % order,
                       'lubchenko05@gmail.com',
                       to=["lubchenko0005@gmail.com", "volodin.yalta.ua@gmail.com "])
    msg.content_subtype = "html"
    msg.send()