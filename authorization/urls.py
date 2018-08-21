from django.conf.urls import include, url
from authorization import views
from django.contrib.auth import views as auth_views

# keep not using this for the django-registration to work
# app_name = 'authorization'

urlpatterns = [
    # workaround for django-registration issue #106
    # https://github.com/ubernostrum/django-registration/issues/106
    url(
        r'^password/change/auth_password_change_done',
        auth_views.password_change_done,
        name='auth_password_change_done'
    ),
    url(r'^', include('registration.backends.simple.urls')),
    url(r'^change_profile/', views.change_profile, name='change_profile'),
    url(r'^profile/', views.change_profile, name="change_profile_alias"),
    url(r'^changed_profile/', views.changed_profile, name='changed_profile'),
]
