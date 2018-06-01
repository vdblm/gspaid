from django.conf.urls import url
from management import views

app_name = 'management'

urlpatterns = [
    url(r'^contact_admin', views.contact_admin, name='contact_admin'),
]
