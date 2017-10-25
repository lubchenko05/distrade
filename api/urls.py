from django.conf.urls import url

from .views import (
    CreateUserView,
    create_category,
    ListCategoryView,
    DetailCategoryView,
    DetailProviderView,
    DetailProductView,
    ListProductView,
    UpdateUserView,
    get_user_detail,
    get_self_user,
    OrderListView,
    deploy,
    update_category,
    update_category__add_criterion,
    update_category__remove_criterion)


urlpatterns = [
    url(r'^deploy/$', deploy, name='deploy'),
    url(r'^order/$', OrderListView.as_view(), name='order-list'),
    url(r'^user/registration/$', CreateUserView.as_view(), name='create-user'),
    url(r'user/$', get_self_user, name='detail-self'),
    url(r'^user/(?P<pk>[\w-]+)/update/$', UpdateUserView.as_view(), name='update-user'),
    url(r'^user/(?P<pk>[\w-]+)/$', get_user_detail, name='user-detail'),
    url(r'^category/$', ListCategoryView.as_view(), name='category-list'),
    url(r'^category/create/$', create_category, name='category-create'),
    url(r'^category/(?P<pk>[\w-]+)/$', DetailCategoryView.as_view(), name='category-detail'),
    url(r'^category/(?P<pk>[\w-]+)/update/$', update_category, name='category-update'),
    url(r'^category/(?P<pk>[\w-]+)/update/add-criterion/$', update_category__add_criterion, name='category-add-criterion'),
    url(r'^provider/(?P<pk>[\w-]+)/update/remove-criterion/$', update_category__remove_criterion, name='category-remove-criterion'),
    url(r'^product/$', ListProductView.as_view(), name='product-list'),
    url(r'^product/(?P<pk>[\w-]+)/$', DetailProductView.as_view(), name='product-detail'),

]
