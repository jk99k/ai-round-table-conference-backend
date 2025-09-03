import threading
from django.db import connection
from .models import Agent
from .services import generate_persona, search_and_download_image

def run_agent_creation_task(agent_id: int):
    try:
        agent = Agent.objects.get(id=agent_id)
        agent.status = 'GENERATING'
        agent.save()
        persona = generate_persona(agent.name)
        avatar_url = search_and_download_image(agent.name, agent.id)
        agent.persona_prompt = persona
        agent.avatar_url = avatar_url
        agent.status = 'COMPLETED'
        agent.save()
    except Exception as e:
        agent = Agent.objects.get(id=agent_id)
        agent.status = 'FAILED'
        agent.save()
    finally:
        connection.close()
