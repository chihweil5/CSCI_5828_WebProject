from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.post_list, name='post_list'),
    url(r'^post/(?P<pk>\d+)/$', views.post_detail, name='post_detail'),
    url(r'^post/new/$', views.post_new, name='post_new'),
    url(r'^post/(?P<pk>\d+)/edit/$', views.post_edit, name='post_edit'),


    url(r'^post_without/$', views.post_list_without_edit, name='post_list_without_edit'),
    url(r'^post_without/(?P<pk>\d+)/$', views.post_detail_without_edit, name='post_detail_without_edit'),
    url(r'^login_form/$', views.login_form, name='login_form'),
    url(r'^signup/$', views.signup, name='signup'),
]