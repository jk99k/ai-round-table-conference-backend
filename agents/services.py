from google import genai
from mako.template import Template
from ddgs import DDGS
import requests
import os
import logging
import mimetypes

PERSONA_TEMPLATE = """
【議論の仕方】
${debate_style}

【思想・価値観】
${philosophy}

【口調・話し方】
${tone}

【代表的な論文・著書の知識】
${works_knowledge}
"""

PROMPT_TEMPLATE = """
あなたはAIエージェント「${name}」です。
以下のテンプレートの各項目を、${name}の人物像に合わせて200文字以内で埋めてください。

${persona_template}
"""

def generate_persona(name: str) -> str:
    persona_template = Template(PERSONA_TEMPLATE).render(
        debate_style="",
        philosophy="",
        tone="",
        works_knowledge=""
    )
    prompt = Template(PROMPT_TEMPLATE).render(name=name, persona_template=persona_template)
    client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
    response = client.models.generate_content(model="gemini-2.0-flash", contents=prompt)
    if response.candidates and hasattr(response.candidates[0], "content"):
        parts = getattr(response.candidates[0].content, "parts", None)
        if parts and hasattr(parts[0], "text"):
            return parts[0].text.strip()
    return ""

def search_and_download_image(query: str, agent_id: int) -> str | None:
    try:
        results = DDGS().images(
            query=query,
            region="jp-jp",
            safesearch="moderate",
            max_results=3,
        )
        for result in results:
            image_url = result.get('image')
            if image_url:
                try:
                    resp = requests.get(image_url)
                    if resp.status_code == 200:
                        os.makedirs("static/images", exist_ok=True)
                        # クエリパラメータを除去して拡張子取得
                        url_path = image_url.split('?')[0]
                        ext = os.path.splitext(url_path)[-1].lstrip('.')
                        # 拡張子が不明な場合はmimetypesで判定
                        if not ext:
                            ext = mimetypes.guess_extension(resp.headers.get('content-type', ''), strict=False) or 'jpg'
                            ext = ext.lstrip('.')
                        local_path = f"static/images/agent_{agent_id}.{ext}"
                        with open(local_path, "wb") as f:
                            f.write(resp.content)
                        return local_path
                except Exception as e:
                    logger = logging.getLogger('agents.services')
                    logger.warning(f"[AgentService] Failed to download image {image_url} for agent_id={agent_id}: {e}")
        return "static/images/default_avatar.png"
    except Exception as e:
        logger = logging.getLogger('agents.services')
        logger.exception(f"[AgentService] Error searching images for agent_id={agent_id}: {e}")
        return "static/images/default_avatar.png"
