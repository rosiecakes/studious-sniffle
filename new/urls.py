from django.conf.urls import url
from django.contrib import admin

from app import views


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', views.index),
    url(r'^tables/', views.tables),
    url(r'^(?P<shortname>\w+)', views.profile, name='profile'),
]
