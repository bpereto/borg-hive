from django.urls import path
from django.urls import include
from .router import router

urlpatterns = [
    path('', include((router.urls, 'api'), namespace='api')),
]
