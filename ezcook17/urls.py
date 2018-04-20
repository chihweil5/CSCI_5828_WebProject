from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^post/$', views.post_list, name='post_list'),
    url(r'^post/(?P<pk>\d+)/$', views.post_detail, name='post_detail'),
    url(r'^post/new/$', views.post_new, name='post_new'),
    url(r'^post/(?P<pk>\d+)/edit/$', views.post_edit, name='post_edit'),


    url(r'^main/$', views.post_list_without_edit, name='post_list_without_edit'),
    url(r'^post_without/(?P<pk>\d+)/$', views.post_detail_without_edit, name='post_detail_without_edit'),
    url(r'^login/$', views.login_form, name='login_form'),
    url(r'^signup/$', views.signup, name='signup'),
    url(r'^logout/$', views.logout_form, name='logout_form'),
    url(r'^mystock/$', views.my_stock, name='my_stock'),
    url(r'^ingredient/new$', views.add_ingredient, name='add_ingredient'),
    # url(r'^ingredient/edit/(?P<name>\w+)/$', views.edit_ingredient, name='edit_ingredient'),
    url(r'^ingredient/edit/(?P<name>\w+)/$', views.edit_ingredient, name='edit_ingredient'),
]
