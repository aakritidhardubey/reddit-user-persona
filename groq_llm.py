import os
import json
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client=OpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1"
)

def generate_prompt(posts,comments):
    return f"""
You are an AI tasked with building a Reddit user persona from the following posts and comments.

Create a detailed persona that includes:

- Demographics (age estimate, location hints, gender indicators)
- Interests & hobbies
- Personality traits
- Activity patterns (posting frequency, preferred subreddits)
- Career interests and professional background
- Technical skills and expertise
- Social behavior and interaction patterns

Use **direct quotes from posts or comments to cite** evidence for each characteristic.
---

POSTS:
{chr(10).join(posts[:10])}
---

COMMENTS:
{chr(10).join(comments[:10])}
"""
def generate_structured_prompt(text_persona):
    return f"""
Convert the following user persona into a JSON object with these fields:

{{
  "demographics": {{
    "age": "...",
    "location": "...",
    "gender": "..."
  }},
  "interests": [...],
  "personality_traits": [...],
  "activity_patterns": {{
    "posting_frequency": "...",
    "top_subreddits": [...]
  }},
  "career": "...",
  "technical_skills": [...],
  "social_behavior": "...",
  "citations": {{
    "demographics": "...",
    "interests": "...",
    "personality_traits": "...",
    "activity_patterns": "...",
    "career": "...",
    "technical_skills": "...",
    "social_behavior": "..."
  }}
}}

Return only valid JSON — do not include explanations or markdown.

---

{text_persona}
"""


def generate_persona(posts,comments):
    prompt=generate_prompt(posts,comments)

    response=client.chat.completions.create(
        model="llama3-70b-8192",
        messages=[
            {"role":"user","content":prompt}
        ],
        temperature=0.7
    )
    persona_text =response.choices[0].message.content.strip()

    struct_prompt = generate_structured_prompt(persona_text)
    struct_response = client.chat.completions.create(
        model="llama3-70b-8192",
        messages=[{"role": "user", "content": struct_prompt}],
        temperature=0.3
    )

    try:
        persona_json = json.loads(struct_response.choices[0].message.content)
    except json.JSONDecodeError:
        persona_json = {
            "error": "Failed to parse JSON from model output.",
            "raw_output": struct_response.choices[0].message.content
        }

    return persona_text, persona_json