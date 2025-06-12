# chatbot/models.py

from django.db import models

class ChatNode(models.Model):
    title = models.CharField()
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='children')
    is_answer = models.BooleanField(default=False)
    order = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title



class UserQuery(models.Model):
    user_id = models.IntegerField(null=True, blank=True)
    name = models.CharField(max_length=100, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    role = models.CharField(max_length=50, null=True, blank=True)

    # ✅ Replace `selected_option` with `conversation` as JSONField
    conversation = models.JSONField(null=True, blank=True)  # use this in Django 3.1+

    query_text = models.TextField(blank=True, null=True)
    satisfied = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.query_text[:50]}"
