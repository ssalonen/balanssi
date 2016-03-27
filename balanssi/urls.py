from __future__ import absolute_import
from django.conf.urls import url

from balanssi import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^transactions.csv$', views.TransactionsView.as_view()),
    url(r'^vis$', views.vis),
]
