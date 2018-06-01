from django.conf.urls import include, url
from authorization import views

app_name = 'authorization'

urlpatterns = [
    url(r'^', include('registration.backends.simple.urls')),
]
