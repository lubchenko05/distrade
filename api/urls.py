from django.conf.urls import url

from api.views import CreateUserView


urlpatterns = [
    url(r'^registration/$', CreateUserView.as_view(), name='registration'),
]
