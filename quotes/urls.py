from django.conf.urls import url, include
from django.urls import path
from rest_framework import routers
from . import views

# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'all', views.QuotesViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    url(r'^', include(router.urls)),
    path('random', views.random_quote),
    url(r'quote/(?P<id>[0-9]+)', views.get_quote),
]

app_name = 'quotes'
