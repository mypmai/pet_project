from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^main$', views.main),
    url(r'^addpet$', views.addpet),
    url(r'^createpet$',views.createpet),
    url(r'^delete/(?P<id>\d+)$',views.delete),
    url(r'^show/(?P<id>\d+)$',views.show),
]
