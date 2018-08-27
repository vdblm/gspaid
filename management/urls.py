from django.conf.urls import url
from management import views

app_name = 'management'

urlpatterns = [
    url(r'^add_request_type', views.add_request_type, name='add_request_type'),
    url(r'^add_exchange_request_type', views.add_exchange_request_type, name='add_exchange_request_type'),
    url(r'^comments', views.comments, name='comments'),
    url(r'^management_dashboard', views.management_dashboard, name='management_dashboard'),
    url(r'^manage_profile/([0-9]+)', views.manage_profile, name='manage_profile'),
    url(r'^management_wallet/$', views.management_wallet, name='management_wallet'),
    url(r'^users/', views.management_users, name='management_users'),
    url(r'^employees/', views.management_employees, name='management_employees'),
    url(r'^requests_history/', views.requests_history, name='requests'),
    url(r'^transaction/([0-9]+)/$', views.transaction, name='transaction'),
    url(r'^currency_transactions/$', views.currency_transactions, name='currency_transactions'),
]
