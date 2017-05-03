from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^registration$', views.registration),
    url(r'^login$', views.login),
    url(r'^logout$', views.logout),
    url(r'^books$', views.books),
    url(r'^books/add$', views.add, name='add'),
    url(r'^add_book$', views.add_book),
    url(r'^users/(?P<id>\d+)$', views.users),
    url(r'^add_review/(?P<id>\d+)/(?P<bid>\d+)$', views.review)
]
