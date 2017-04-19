from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^registration$', views.registration),
    url(r'^login$', views.login),
    url(r'^logout$', views.logout),
    url(r'^success$', views.success),
    url(r'^quotes/(?P<id>\d+)$', views.quotes),
    url(r'^favorite/(?P<id>\d+)/(?P<qid>\d+)$', views.favorite),
    url(r'^remove/(?P<id>\d+)/(?P<qid>\d+)$', views.remove),
    url(r'^users/(?P<id>\d+)$', views.users)
]
