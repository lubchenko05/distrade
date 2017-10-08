from django.conf.urls import url

from .views import (
    CreateUserView,
    ListCategoryView,
    DetailCategoryView,
    DetailProviderView,
    DetailProductView,
    ListProductView,
    UpdateUserView,
    get_user_detail)


urlpatterns = [
    url(r'^user/registration/$', CreateUserView.as_view(), name='create-user'),
    url(r'^user/(?P<pk>[\w-]+)/update/$', UpdateUserView.as_view(), name='update-user'),
    url(r'^user/(?P<pk>[\w-]+)/$', get_user_detail, name='detail-user'),
    url(r'^category/$', ListCategoryView.as_view(), name='category-list'),
    url(r'^category/(?P<name>[\w-]+)$', DetailCategoryView.as_view(), name='category-detail'),
    url(r'^provider/(?P<name>[\w-]+)$', DetailProviderView.as_view(), name='provider-detail'),
    url(r'^product/$', ListProductView.as_view(), name='product-list'),
    url(r'^product/(?P<name>[\w-]+)$', DetailProductView.as_view(), name='product-detail'),

]
