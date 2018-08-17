from django.conf.urls import url, include

from workflow import views

app_name='workflow'

urlpatterns = [
    url(r'^dashboard/', views.costumer_dashboard, name='dashboard'),
    url(r'^requests/', views.requests, name='requests'),
    url(r'^costumer_requests/', views.costumer_new_request, name='costumer_requests'),
]
