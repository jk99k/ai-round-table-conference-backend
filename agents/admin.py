from django.contrib import admin

from agents.models import Agent

# Register your models here.
@admin.register(Agent)
class AgentAdmin(admin.ModelAdmin):
	list_display = ("id", "name", "persona_prompt", "avatar_url", "status", "created_at")