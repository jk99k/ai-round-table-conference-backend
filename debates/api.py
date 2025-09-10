from ninja import Router
from ninja_jwt.authentication import JWTAuth
from django.shortcuts import get_object_or_404
from .models import Debate, DebateStatus, Message
from .schemas import DebateCreateSchema, DebateDeleteIn, DebateOutSchema, MessageOutSchema, InterruptDebateIn
from .tasks import generate_debate_turn
from agents.models import Agent

router = Router(auth=JWTAuth(), tags=["debates"])


@router.post("", response={201: DebateOutSchema, 400: dict})
def create_debate(request, data: DebateCreateSchema):
    try:
        debate = Debate.objects.create(
            topic=data.topic,
            status=DebateStatus.IN_PROGRESS
        )
        agents = Agent.objects.filter(id__in=data.agent_ids)
        debate.agents.set(agents)
        generate_debate_turn(debate.id, schedule=5)
        # DebateOutSchemaはfrom_ormで生成
        return 201, DebateOutSchema.from_orm(debate)
    except Exception as e:
        return 400, {"error": str(e)}


@router.post("/{debate_id}/end", response={200: DebateOutSchema, 404: dict})
def end_debate(request, debate_id: int):
    debate = Debate.objects.filter(id=debate_id).first()
    if not debate:
        return 404, {"error": "Debate not found"}
    debate.status = DebateStatus.TERMINATED_BY_USER
    debate.save()
    return 200, DebateOutSchema.from_orm(debate)


@router.get("", response=list[DebateOutSchema])
def list_debates(request):
    debates = Debate.objects.all().order_by('-created_at')
    debate_out_list = []
    for debate in debates:
        agents = list(debate.agents.all().order_by('id'))
        messages = list(debate.messages.order_by('turn'))
        # agentがNoneの場合は空のAgentOutSchemaを返す
        for msg in messages:
            if msg.agent is None:
                from agents.models import Agent
                dummy_agent = Agent(id=0, name=msg.agent_name or "Human", status="COMPLETED", persona_prompt="", avatar_url="", created_at=msg.created_at, updated_at=msg.created_at)
                msg.agent = dummy_agent
        if agents:
            if messages:
                next_idx = (messages[-1].turn) % len(agents)
            else:
                next_idx = 0
            next_agent = agents[next_idx]
            next_agent_id = next_agent.id
            next_agent_name = next_agent.name
        else:
            next_agent_id = None
            next_agent_name = None
        debate_out = DebateOutSchema.from_orm(debate)
        debate_out.next_agent_id = next_agent_id
        debate_out.next_agent_name = next_agent_name
        debate_out_list.append(debate_out)
    return debate_out_list


@router.get("/{debate_id}", response={200: DebateOutSchema, 404: dict})
def get_debate(request, debate_id: int):
    debate = Debate.objects.filter(id=debate_id).first()
    if not debate:
        return 404, {"error": "Debate not found"}
    agents = list(debate.agents.all().order_by('id'))
    messages = list(debate.messages.order_by('turn'))
    for msg in messages:
        if msg.agent is None:
            from agents.models import Agent
            dummy_agent = Agent(id=0, name=msg.agent_name or "Human", status="COMPLETED", persona_prompt="", avatar_url="", created_at=msg.created_at, updated_at=msg.created_at)
            msg.agent = dummy_agent
    if agents:
        if messages:
            next_idx = (messages[-1].turn) % len(agents)
        else:
            next_idx = 0
        next_agent = agents[next_idx]
        next_agent_id = next_agent.id
        next_agent_name = next_agent.name
    else:
        next_agent_id = None
        next_agent_name = None
    debate_out = DebateOutSchema.from_orm(debate)
    debate_out.next_agent_id = next_agent_id
    debate_out.next_agent_name = next_agent_name
    return 200, debate_out

@router.delete("", response={200: dict, 400: dict})
def delete_debates(request, data: DebateDeleteIn):
    try:
        deleted, _ = Debate.objects.filter(id__in=data.ids).delete()
        return 200, {"deleted": deleted}
    except Exception as e:
        return 400, {"error": str(e)}

@router.post("/{debate_id}/interrupt", response={201: MessageOutSchema, 404: dict, 400: dict})
def interrupt_debate(request, debate_id: int, data: InterruptDebateIn):
    """
    人間による割り込み指示を議論プロセスに追加し、AIが次ターンで認識できるようにする。
    """
    debate = Debate.objects.filter(id=debate_id).first()
    if not debate:
        return 404, {"error": "Debate not found"}
    try:
        # 人間メッセージとして保存（agent_name='Human'）
        message = Message.objects.create(
            debate=debate,
            agent_name="Human",
            content=data.content,
            turn=debate.messages.count() + 1
        )
        return 201, MessageOutSchema.from_orm(message)
    except Exception as e:
        return 400, {"error": str(e)}