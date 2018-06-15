from django.conf.urls import include, url
from authorization import views


urlpatterns = [
    url(r'^', include('registration.backends.simple.urls')),
]
