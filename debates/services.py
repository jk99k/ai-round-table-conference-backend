from .schemas import ModeratorResponse
from .models import Debate, Message
from agents.models import Agent
from mako.template import Template
from google import genai
import os

def determine_next_turn(debate: Debate) -> ModeratorResponse:
    messages = list(debate.messages.select_related('agent').order_by('turn'))
    agents = list(debate.agents.all().order_by('id'))
    if not agents:
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
    prompt = template.render(
        debate=debate,
        agents=agents,
        messages=messages,
        next_agent=next_agent
    )

    client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
        config={
            "response_mime_type": "application/json",
            "response_schema": ModeratorResponse,
        },
    )
    return response.parsed

    client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
        config={
            "response_mime_type": "application/json",
            "response_schema": ModeratorResponse,
        },
    )
    # response.textはJSON文字列、response.parsedはModeratorResponseインスタンス
    result = response.parsed
    result.agent_id = next_agent.id
    result.agent_name = next_agent.name
    return result
