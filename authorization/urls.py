from django.conf.urls import include, url
from authorization import views


urlpatterns = [
    url(r'^', include('registration.backends.simple.urls')),
    url(r'^change_password', views.change_password),
    url(r'^changed_password', views.changed_password),
    url(r'^change_profile', views.change_profile),
    url(r'^changed_profile', views.changed_profile),
]
