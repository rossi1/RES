from django.urls  import path

from . import views

app_name = 'messager'
urlpatterns = [
    path('', views.MessagesListView.as_view(), name='messages_list'),
    path('send-message/', views.SendMessage.as_view(), name='send_message'),
    path('receive-message/',
        views.receive_message, name='receive_message'),
    path('<int:pk>/', views.ConversationListView.as_view(),
        name='conversation_detail'),
]
