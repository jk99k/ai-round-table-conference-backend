from google import genai
from mako.template import Template
import wikipedia
import requests
import os

def generate_persona(name: str) -> str:
    template = Template("あなたはAIエージェント「${name}」です。個性と役割を200文字以内で説明してください。")
    print(template)
    prompt = template.render(name=name)
    genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
    model = genai.GenerativeModel("gemini-pro")
    response = model.generate_content([prompt])
    return response.text.strip() if hasattr(response, 'text') else str(response)

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
