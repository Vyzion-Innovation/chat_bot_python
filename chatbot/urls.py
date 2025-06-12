from django.urls import path, include
from .views import ChatNodeViewSet, chatbot_ui, save_query
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'nodes', ChatNodeViewSet)

urlpatterns = [
    path('', chatbot_ui, name='chatbot-ui'),         # ✅ Show chatbot UI on /
    path('api/', include(router.urls)),              # ✅ APIs under /api/
    path('api/save-query/', save_query),
]
