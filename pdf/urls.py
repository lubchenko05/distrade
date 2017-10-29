from django.conf.urls import url

from .views import get_check


urlpatterns = [
    url(r'^order/(?P<pk>[\w-]+)/check/$', get_check, name='order-check'),

]
