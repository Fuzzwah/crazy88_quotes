from django.conf.urls import url, include
from django.urls import path
from rest_framework import routers
from . import views

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('random', views.random_quote),
    path('quote', views.get_quote),
    path('search', views.search_quote),
    path('psearch', views.search_pquote),
    path('add', views.add_quote),
    path('add_shortcut', views.add_quote_shortcut),


]

app_name = 'quotes'
