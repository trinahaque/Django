from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^registration$', views.registration),
    url(r'^login$', views.login),
    url(r'^logout$', views.logout),
    url(r'^success$', views.success),
    url(r'^add/(?P<id>\d+)$', views.add),
    url(r'^edit/(?P<aid>\d+)/(?P<id>\d+)$', views.edit, name='edit'),
    url(r'^update/(?P<aid>\d+)/(?P<id>\d+)$', views.update),
    url(r'^delete/(?P<aid>\d+)/(?P<id>\d+)$', views.delete)
]
