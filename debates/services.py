from .schemas import ModeratorResponse
from .models import Debate, Message
from agents.models import Agent
from mako.template import Template
from google import genai
import os
import logging

def determine_next_turn(debate: Debate) -> ModeratorResponse:
    logger = logging.getLogger('debates.services')
    messages = list(debate.messages.select_related('agent').order_by('turn'))
    # 未使用のHumanメッセージ（割り込み指示）があれば取得
    human_message = debate.messages.filter(agent_name='Human', used=False).order_by('-created_at').first()
    agents = list(debate.agents.all().order_by('id'))
    if not agents:
        logger.error(f"[DebateService] No agents assigned to debate {debate.id}")
        raise Exception('No agents assigned to debate')
    # ターン番号から次のエージェントを決定
    if messages:
        next_idx = (messages[-1].turn) % len(agents)
    else:
        next_idx = 0
    next_agent = agents[next_idx]
    # Makoテンプレートでプロンプト生成
    template_path = os.path.join(os.path.dirname(__file__), "templates", "debate_prompt.mako")
    template = Template(filename=template_path, input_encoding="utf-8")
    # プロンプトに人間指示を含める
    if human_message:
        prompt = template.render(
            debate=debate,
            agents=agents,
            messages=messages,
            next_agent=next_agent,
            human_instruction=human_message.content
        )
        # 指示を使ったらused=Trueに
        human_message.used = True
        human_message.save()
    else:
        prompt = template.render(
            debate=debate,
            agents=agents,
            messages=messages,
            next_agent=next_agent
        )
    logger.info(f"[DebateService] Prompt for debate_id={debate.id}:\n{prompt}")

    try:
        client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
            config={
                "response_mime_type": "application/json",
                "response_schema": ModeratorResponse,
            },
        )
        moderator_response = response.parsed
        # Geminiの返却値にagent_id/agent_nameを補完
        moderator_response.agent_id = next_agent.id
        moderator_response.agent_name = next_agent.name
        logger.info(f"[DebateService] Gemini response for debate_id={debate.id}: {response.text}")
        return moderator_response
    except Exception as e:
        logger.exception(f"[DebateService] Gemini API error for debate_id={debate.id}: {e}")
        raise
