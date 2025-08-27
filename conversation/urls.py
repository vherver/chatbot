from django.urls import path
from conversation.views import MessageView

urlpatterns = [
    path('message', MessageView.as_view(), name='send-message'),
]