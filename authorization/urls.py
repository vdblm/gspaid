from django.conf.urls import include, url
from authorization import views
import registration.auth_urls_functions

urlpatterns = [
    url(r'^', include('registration.backends.simple.urls')),
    url(r'^change_profile/', views.change_profile, name='change_profile'),
    url(r'^changed_profile/', views.changed_profile, name='changed_profile'),
    url(r'^profile/', views.profile, name="profile"),
]
