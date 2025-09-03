from google import genai
from mako.template import Template
import wikipedia
import requests
import os

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
        page = wikipedia.page(query)
        if page.images:
            image_url = page.images[0]
            resp = requests.get(image_url)
            if resp.status_code == 200:
                os.makedirs("static/images", exist_ok=True)
                ext = image_url.split('.')[-1]
                local_path = f"static/images/agent_{agent_id}.{ext}"
                with open(local_path, "wb") as f:
                    f.write(resp.content)
                return local_path
    except Exception:
        pass
    return None
