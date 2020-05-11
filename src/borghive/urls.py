from django.urls import path
from django.views.generic.base import RedirectView

from borghive.views import (NotificationUpdateView, NotificationCreateView, NotificationDeleteView,
                            NotificationListView,
                            RepositoryCreateView, RepositoryDeleteView,
                            RepositoryDetailView, RepositoryListView,
                            RepositoryUpdateView, SSHPublicKeyCreateView,
                            SSHPublicKeyDeleteView, SSHPublicKeyListView,
                            SSHPublicKeyUpdateView)

urlpatterns = [
    path('', RedirectView.as_view(url='repository/list', permanent=False), name='index'),
    path('repository/list/', RepositoryListView.as_view(), name='repository-list'),
    path('repository/detail/<int:pk>', RepositoryDetailView.as_view(), name='repository-detail'),
    path('repository/create/', RepositoryCreateView.as_view(), name='repository-create'),
    path('repository/delete/<int:pk>', RepositoryDeleteView.as_view(), name='repository-delete'),
    path('repository/update/<int:pk>', RepositoryUpdateView.as_view(), name='repository-update'),
    path('keys/list/', SSHPublicKeyListView.as_view(), name='key-list'),
    path('keys/create/', SSHPublicKeyCreateView.as_view(), name='key-create'),
    path('keys/delete/<int:pk>', SSHPublicKeyDeleteView.as_view(), name='key-delete'),
    path('keys/update/<int:pk>', SSHPublicKeyUpdateView.as_view(), name='key-update'),
    path('notifications/list/', NotificationListView.as_view(), name='notification-list'),
    path('notifications/create/<str:n_type>', NotificationCreateView.as_view(), name='notification-create'),
    path('notifications/update/<int:pk>', NotificationUpdateView.as_view(), name='notification-update'),
    path('notifications/delete/<int:pk>', NotificationDeleteView.as_view(), name='notification-delete')
]
