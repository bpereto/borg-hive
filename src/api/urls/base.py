from django.urls import path
from django.urls import include
from api.router import router

urlpatterns = [
    path('', include((router.urls, 'api'), namespace='api')),
    path('schema/', include('api.urls.schema'))
]
