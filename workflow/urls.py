from django.conf.urls import url, include

from workflow import views

app_name = 'workflow'

urlpatterns = [
    url(r'^dashboard/', views.costumer_dashboard, name='dashboard'),
    url(r'^requests_history/(?P<user_id>[0-9]+)/$', views.user_requests_history, name='requests_history_id'),
    url(r'^requests_history/', views.user_requests_history, name='requests_history'),
    url(r'^request_history/(?P<num>[0-9]+)/$', views.user_request_history, name='request_history'),
    url(r'^exchange_request_history/(?P<num>[0-9]+)/$', views.user_exchange_request_history,
        name='exchange_request_history'),
    url(r'^internal_payment_history/(?P<num>[0-9]+)/$', views.user_anonymous_request_history,
        name='anonymous_request_history'),
    url(r'^new_request/(?P<num>[0-9]+)/$', views.user_new_request, name='new_request'),
    url(r'^new_exchange_request/(?P<num>[0-9]+)/$', views.user_new_exchange_request, name='new_exchange_request'),
    url(r'^request_types/', views.user_request_types, name='request_types'),
    url(r'^exchange_request_types/', views.user_exchange_request_types, name='exchange_request_types'),
    url(r'^check_requests/', views.check_requests, name='check_requests'),
    url(r'^check_request/(?P<num>[0-9]+)/$', views.check_request, name='check_request'),
]
