from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^registration$', views.registration),
    url(r'^login$', views.login),
    url(r'^logout$', views.logout),
    url(r'^success$', views.success),
    url(r'^travels/add$', views.add, name="add"),
    url(r'^add$', views.create_trip)
    # url(r'^add/(?P<id>\d+)$', views.add_trip),
]
