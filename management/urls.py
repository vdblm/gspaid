from django.conf.urls import url
from management import views

app_name = 'management'

urlpatterns = [
    url(r'^contact_admin', views.contact_admin, name='contact_admin'),
    url(r'^add_request_type', views.add_request_type, name='add_request_type'),
    url(r'^settings_changed', views.settings_changed, name="settings_changed"),
    url(r'^settings', views.settings, name='settings'),
    url(r'^management_dashboard', views.management_dashboard, name='management_dashboard'),
    url(r'^manage_profile/([0-9]+)', views.manage_profile, name='manage_profile'),
]
