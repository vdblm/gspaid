from django.conf.urls import url, include

from workflow import views

app_name='workflow'

urlpatterns = [
    url(r'^dashboard/', views.costumer_dashboard, name='dashboard'),
    url(r'^requests_history/', views.user_requests_history, name='requests_history'),
    url(r'^request_history/(?P<num>[0-9]+)/$', views.user_request_history, name='request_history'),
    url(r'^new_request/(?P<num>[0-9]+)/$', views.user_new_request, name='new_request'),
    url(r'^request_types/', views.user_request_types, name='request_types'),
]
