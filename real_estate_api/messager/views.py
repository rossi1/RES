from django.contrib.auth import get_user_model
from django.views.decorators.http import require_http_methods
from django.db.models import Q


from rest_framework.generics import ListAPIView, GenericAPIView
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication
from rest_framework.response import Response

from accounts.authentication import JwtAuthentication

from .models import Message
from .serializer import ChatSerializer, Chat


class MessagesListView(ListAPIView):
    
    """CBV to render the inbox, showing by default the most recent
    conversation as the active on
    .
    """
    queryset = Message
    serializer_class = ChatSerializer
    permission_classes = (IsAuthenticated, )


    """
    def get_queryset(self):
        context = {}
        context['users_list']  = get_user_model().objects.filter(is_active=True).exclude(
            username=self.request.user).order_by('username')
        last_conversation = Message.objects.get_most_recent_conversation(
            self.request.user
        )
        context['active'] = last_conversation.username
        return context

    """
  
  
  
    def get_queryset(self):
        
        active_user = Message.objects.filter(Q(sender=self.request.user) | Q(recipient=self.request.user))
        return  active_user #Message.objects.get_conversation(active_user, self.request.user)


class ConversationListView(MessagesListView):
    """CBV to render the inbox, showing an specific conversation with a given
    user, who requires to be active too."""
    

    def get_queryset(self):
        active_user = get_user_model().objects.get(
            pk=self.kwargs["pk"])
        return Message.objects.get_conversation(active_user, self.request.user)

class SendMessage(GenericAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = Chat

    def post(self, request, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        sender = request.user
        recipient_username = serializer.validated_data['to']
        recipient = get_user_model().objects.get(email__iexact=recipient_username)
        message = serializer.validated_data['message']
        if len(message.strip()) == 0:
            return Response({})
            
        if sender != recipient:
            msg = Message.send_message(sender, recipient, message)
            return Response({'message': msg})
            
        return Response({})


    
    
    



@permission_classes([IsAuthenticated,])
@api_view(['POST'])
def send_message(request):
    """AJAX Functional view to recieve just the minimum information, process
    and create the new message and return the new data to be attached to the
    conversation stream."""
    sender = request.user
    recipient_username = request.POST.get('to')
    recipient = get_user_model().objects.get(email__iexact=recipient_username)
    message = request.POST.get('message')
    if len(message.strip()) == 0:
        return Response({})

    if sender != recipient:
        msg = Message.send_message(sender, recipient, message)
        return Response({'message': msg})

    return Response({})

@permission_classes([IsAuthenticated,])
@api_view(['GET'])
def receive_message(request):
    """Simple AJAX functional view to return a rendered single message on the
    receiver side providing realtime connections."""
    message_id = request.GET.get('message_id')
    message = Message.objects.get(pk=message_id)
    return  Response({'message': message})
