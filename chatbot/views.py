from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from .models import ChatNode, UserQuery
from .serializers import ChatNodeSerializer

import os
import json
import string
import nltk
from nltk.tokenize import TreebankWordTokenizer  # ✅ No punkt dependency
from .badwords import BAD_WORDS

# ✅ Optional: set custom nltk_data path if you still want to include it
NLTK_DATA_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'nltk_data')
if os.path.exists(NLTK_DATA_PATH):
    nltk.data.path.append(NLTK_DATA_PATH)


class ChatNodeViewSet(viewsets.ModelViewSet):
    queryset = ChatNode.objects.all()
    serializer_class = ChatNodeSerializer

    @action(detail=False, methods=['get'], url_path='children')
    def get_children(self, request):
        parent_id = request.query_params.get('parent')
        if parent_id is None:
            return Response({"error": "Missing parent ID"}, status=400)

        nodes = ChatNode.objects.filter(parent_id=parent_id).order_by('order')
        serializer = ChatNodeSerializer(nodes, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], url_path='start')
    def get_start_nodes(self, request):
        root_nodes = ChatNode.objects.filter(parent=None).order_by('order')
        serializer = ChatNodeSerializer(root_nodes, many=True)
        return Response(serializer.data)


def chatbot_ui(request):
    return render(request, 'chatbot_ui.html')


@csrf_exempt
def save_query(request):
    if request.method != 'POST':
        return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)

    try:
        data = json.loads(request.body)
        query_text = data.get('query_text', '')

        # ✅ Clean and tokenize text using TreebankWordTokenizer (no punkt)
        cleaned = query_text.lower()
        cleaned = cleaned.translate(str.maketrans('', '', string.punctuation))
        tokenizer = TreebankWordTokenizer()
        tokens = tokenizer.tokenize(cleaned)

        # ✅ Check for inappropriate words
        bad_used = BAD_WORDS.intersection(tokens)
        if bad_used:
            return JsonResponse({
                'status': 'error',
                'message': f"Inappropriate language detected: {', '.join(bad_used)}. Please submit a genuine query."
            }, status=400)

        # ✅ Save if clean
        UserQuery.objects.create(
            user_id=data.get('userId'),
            name=data.get('name'),
            email=data.get('email'),
            role=data.get('role'),
            conversation=data.get('conversation'),
            query_text=query_text,
            satisfied=data.get('satisfied', False)
        )

        return JsonResponse({'status': 'success'})

    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
