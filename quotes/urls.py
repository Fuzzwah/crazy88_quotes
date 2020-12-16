from django.conf.urls import url, include
from rest_framework import routers
from . import views

# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'quotes', views.QuotesViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^random$', views.RandomQuoteView.as_view(), name='random'),
    url(r'^quote/(?P<id>[0-9]+)/$', views.QuoteView.as_view(), name='quote'),
]

app_name = 'quotes'
