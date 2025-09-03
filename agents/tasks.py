from django.db import connection
from .models import Agent
from .services import generate_persona, search_and_download_image
import logging

def run_agent_creation_task(agent_id: int):
    try:
        logger = logging.getLogger('agents.tasks')
        agent = Agent.objects.get(id=agent_id)
        agent.status = 'GENERATING'
        agent.save()
        logger.info(f"[AgentTask] Generating persona for: {agent.name}")
        persona = generate_persona(agent.name)
        avatar_url = search_and_download_image(agent.name, agent.id)
        logger.info(f"[AgentTask] Avatar URL result: {avatar_url}")
        agent.persona_prompt = persona
        agent.avatar_url = avatar_url
        agent.status = 'COMPLETED'
        agent.save()
    except Exception as e:
        logger.exception(f"[AgentTask] Error for agent_id={agent_id}: {e}")
        agent = Agent.objects.get(id=agent_id)
        agent.status = 'FAILED'
        agent.save()
    finally:
        connection.close()
