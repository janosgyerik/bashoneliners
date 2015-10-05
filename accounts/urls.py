from django.conf.urls import url
from accounts import views

urlpatterns = [
    url(r'^login/$', views.login, name='login'),
    url(r'^logout/$', views.logout, name='logout'),
    url(r'^status/$', views.status, name='status'),
]
