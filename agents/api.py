from ninja import Router
from ninja_jwt.authentication import JWTAuth
from django.shortcuts import get_object_or_404
from .models import Agent
from .schemas import AgentCreateSchema, AgentDeleteIn, AgentOutSchema
from .tasks import run_agent_creation_task
import threading

router = Router(auth=JWTAuth(), tags=["agents"])

@router.post("", response=AgentOutSchema)
def create_agent(request, data: AgentCreateSchema):
    agent = Agent.objects.create(
        user=request.user,
        name=data.name,
        status='PENDING'
    )
    threading.Thread(target=run_agent_creation_task, args=(agent.id,), daemon=True).start()
    return agent

@router.get("", response=list[AgentOutSchema])
def list_agents(request):
    return Agent.objects.filter(user=request.user).order_by('-created_at')

@router.get("/{agent_id}", response=AgentOutSchema)
def get_agent(request, agent_id: int):
    agent = get_object_or_404(Agent, id=agent_id, user=request.user)
    return agent

@router.delete("", response={200: dict, 400: dict})
def delete_agents(request, data: AgentDeleteIn):
    try:
        deleted, _ = Agent.objects.filter(id__in=data.ids).delete()
        return 200, {"deleted": deleted}
    except Exception as e:
        return 400, {"error": str(e)}
