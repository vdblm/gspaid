from django.conf.urls import include, url
from authorization import views

urlpatterns = [
    # Other URL patterns ...
    url(r'^/', views.index, 'index'),
    url(r'^', include('registration.backends.simple.urls')),
    # More URL patterns ...
]
