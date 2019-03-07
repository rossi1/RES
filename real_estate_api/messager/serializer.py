from rest_framework import serializers

from .models import Message


class ChatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = '__all__'


class Chat(serializers.Serializer):
    to = serializers.EmailField()
    message = serializers.CharField(max_length=200)