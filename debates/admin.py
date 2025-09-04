# Django admin登録
from django.contrib import admin
from .models import Debate, Message

@admin.register(Debate)
class DebateAdmin(admin.ModelAdmin):
	list_display = ("id", "topic", "status", "created_at", "updated_at")
	filter_horizontal = ("agents",)

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
	list_display = ("id", "debate", "agent", "content", "turn", "created_at")
	list_filter = ("debate", "agent")