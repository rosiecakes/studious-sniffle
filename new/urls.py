from django.conf.urls import url
from django.contrib import admin
from django.views.generic import TemplateView

from app import views


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', views.index),
    url(r'^(?P<shortname>\w+)', views.profile),
]
