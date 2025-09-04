from background_task import background
from django.db import transaction
from .models import Debate, DebateStatus, Message
from .services import determine_next_turn
import logging

@background(schedule=5)
def generate_debate_turn(debate_id):
    logger = logging.getLogger('debates.tasks')
    logger.info(f"[DebateTask] Start generate_debate_turn for debate_id={debate_id}")
    try:
        debate = Debate.objects.get(id=debate_id)
        if debate.status != DebateStatus.IN_PROGRESS:
            logger.info(f"[DebateTask] Debate {debate_id} status is not IN_PROGRESS ({debate.status}), skipping.")
            return  # 停止・完了なら何もしない

        last_message = debate.messages.order_by('-turn').first()
        logger.info(f"[DebateTask] Last message: {last_message}")
        moderator_response = determine_next_turn(debate=debate)
        logger.info(f"[DebateTask] ModeratorResponse: {moderator_response}")

        next_turn = (last_message.turn + 1) if last_message else 1
        Message.objects.create(
            debate=debate,
            agent_id=moderator_response.agent_id,
            content=getattr(moderator_response, 'statement', getattr(moderator_response, 'content', '')),
            turn=next_turn
        )
        logger.info(f"[DebateTask] Message created for agent_id={moderator_response.agent_id}, turn={next_turn}")

        if moderator_response.conclusion_reason:
            debate.status = DebateStatus.COMPLETED_AI
            debate.save()
            logger.info(f"[DebateTask] Debate {debate_id} completed by AI. Reason: {moderator_response.conclusion_reason}")
            return

        # 10〜15秒後に再スケジュール
        generate_debate_turn(debate_id, schedule=10)
        logger.info(f"[DebateTask] Rescheduled debate_id={debate_id} for next turn.")
    except Exception as e:
        logger.exception(f"[DebateTask] Error in generate_debate_turn for debate_id={debate_id}: {e}")
        try:
            debate = Debate.objects.get(id=debate_id)
            debate.status = DebateStatus.FAILED
            debate.save()
        except Exception:
            pass
