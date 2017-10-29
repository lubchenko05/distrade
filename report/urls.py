from django.conf.urls import url

from .views import get_check, invoice


urlpatterns = [
    url(r'^order/(?P<pk>[\w-]+)/$', get_check, name='order-check'),
    url(r'^invoice/(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d+)/$', invoice, name='invoice'),

]
