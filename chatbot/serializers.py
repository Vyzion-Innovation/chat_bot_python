# chatbot/serializers.py

from rest_framework import serializers
from .models import ChatNode

class ChatNodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatNode
        fields = '__all__'
