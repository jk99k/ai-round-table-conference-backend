from ninja import Router
from ninja_jwt.authentication import JWTAuth
from django.shortcuts import get_object_or_404
from .models import Debate, DebateStatus, Message
from .schemas import DebateCreateSchema, DebateOutSchema, MessageOutSchema
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


@router.post("/{debate_id}/end/", response={200: DebateOutSchema, 404: dict})
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
    return [DebateOutSchema.from_orm(obj) for obj in debates]


@router.get("/{debate_id}", response={200: DebateOutSchema, 404: dict})
def get_debate(request, debate_id: int):
    debate = Debate.objects.filter(id=debate_id).first()
    if not debate:
        return 404, {"error": "Debate not found"}
    return 200, DebateOutSchema.from_orm(debate)

# POST /{debate_id}/next-turn/ は削除
