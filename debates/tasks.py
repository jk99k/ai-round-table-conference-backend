from background_task import background
from django.db import transaction
from .models import Debate, DebateStatus, Message
from .services import determine_next_turn

@background(schedule=5)
def generate_debate_turn(debate_id):
    try:
        debate = Debate.objects.select_for_update().get(id=debate_id)
        if debate.status != DebateStatus.IN_PROGRESS:
            return  # 停止・完了なら何もしない

        last_message = debate.messages.order_by('-turn').first()
        moderator_response = determine_next_turn(debate, last_message)

        next_turn = (last_message.turn + 1) if last_message else 1
        Message.objects.create(
            debate=debate,
            agent_id=moderator_response.agent_id,
            content=moderator_response.content,
            turn=next_turn
        )

        if moderator_response.conclusion_reason:
            debate.status = DebateStatus.COMPLETED_AI
            debate.save()
            return

        # 10〜15秒後に再スケジュール
        generate_debate_turn(debate_id, schedule=10)
    except Exception as e:
        debate = Debate.objects.get(id=debate_id)
        debate.status = DebateStatus.FAILED
        debate.save()
