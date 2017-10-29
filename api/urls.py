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
    create_order,
    DetailOrderView,
    UpdateOrderView,
    CheckListView,
    deploy,
    update_category,
    update_category__add_criterion,
    update_category__remove_criterion,
    update_product__add_like,
    update_product__remove_like, get_check)


urlpatterns = [
    url(r'^deploy/$', deploy, name='deploy'),
    url(r'^order/$', OrderListView.as_view(), name='order-list'),

    url(r'^user/registration/$', CreateUserView.as_view(), name='create-user'),
    url(r'^user/$', get_self_user, name='detail-self'),
    url(r'^user/(?P<pk>[\w-]+)/update/$', UpdateUserView.as_view(), name='update-user'),
    url(r'^user/(?P<pk>[\w-]+)/$', get_user_detail, name='user-detail'),

    url(r'^category/$', ListCategoryView.as_view(), name='category-list'),
    url(r'^category/create/$', create_category, name='category-create'),
    url(r'^category/(?P<pk>[\w-]+)/$', DetailCategoryView.as_view(), name='category-detail'),
    url(r'^category/(?P<pk>[\w-]+)/update/$', update_category, name='category-update'),
    url(r'^category/(?P<pk>[\w-]+)/update/add-criterion/$', update_category__add_criterion, name='category-add-criterion'),
    url(r'^category/(?P<pk>[\w-]+)/update/remove-criterion/$', update_category__remove_criterion, name='category-remove-criterion'),

    url(r'^product/$', ListProductView.as_view(), name='product-list'),
    url(r'^product/(?P<pk>[\w-]+)/$', DetailProductView.as_view(), name='product-detail'),
    url(r'^product/(?P<pk>[\w-]+)/like/$', update_product__add_like, name='product-detail-add-like'),
    url(r'^product/(?P<pk>[\w-]+)/dislike/$', update_product__remove_like, name='product-detail-remove-like'),

    url(r'^order/$', OrderListView.as_view(), name='order-list'),
    url(r'^order/create/$', create_order, name='order-create'),
    url(r'^order/(?P<pk>[\w-]+)/$', DetailOrderView.as_view(), name='order-detail'),
    url(r'^order/(?P<pk>[\w-]+)/update/$', UpdateOrderView.as_view(), name='order-update'),
    url(r'^order/(?P<pk>[\w-]+)/check/$', get_check, name='order-check'),


    url(r'^provider/(?P<name>[\w-]+)/$', DetailProviderView.as_view(), name='provider-detail'),
]
