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
Convert the following user persona into a valid JSON object. Return ONLY the JSON, no explanations, no markdown formatting, no code blocks.

Required JSON structure:
{{
  "demographics": {{
    "age": "age range or estimate",
    "location": "location if mentioned",
    "gender": "gender if determinable"
  }},
  "interests": ["interest1", "interest2", "interest3"],
  "personality_traits": ["trait1", "trait2", "trait3"],
  "activity_patterns": {{
    "posting_frequency": "frequency description",
    "top_subreddits": ["subreddit1", "subreddit2"]
  }},
  "career": "career or profession",
  "technical_skills": ["skill1", "skill2", "skill3"],
  "social_behavior": "description of social behavior",
  "citations": {{
    "demographics": "evidence source",
    "interests": "evidence source",
    "personality_traits": "evidence source",
    "activity_patterns": "evidence source",
    "career": "evidence source",
    "technical_skills": "evidence source",
    "social_behavior": "evidence source"
  }}
}}

Text persona to convert:
{text_persona}

JSON:"""


def clean_json_response(response_text):
    """Clean the JSON response from markdown formatting and other issues"""
    # Remove markdown code blocks
    if "```json" in response_text:
        response_text = response_text.split("```json")[1].split("```")[0]
    elif "```" in response_text:
        # Find the content between backticks
        parts = response_text.split("```")
        # Look for the part that contains JSON (starts with { or [)
        for part in parts:
            part = part.strip()
            if part.startswith('{') or part.startswith('['):
                response_text = part
                break
    
    # Strip whitespace
    response_text = response_text.strip()
    
    return response_text

def generate_persona(posts,comments):
    prompt=generate_prompt(posts,comments)

    response=client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role":"user","content":prompt}
        ],
        temperature=0.7
    )
    persona_text =response.choices[0].message.content.strip()

    struct_prompt = generate_structured_prompt(persona_text)
    struct_response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": struct_prompt}],
        temperature=0.3
    )

    raw_json_response = struct_response.choices[0].message.content
    cleaned_json = clean_json_response(raw_json_response)
    
    try:
        persona_json = json.loads(cleaned_json)
    except json.JSONDecodeError as e:
        print(f"JSON Parse Error: {e}")
        print(f"Raw response: {raw_json_response}")
        print(f"Cleaned response: {cleaned_json}")
        
        # Try to extract JSON from the raw output if it exists
        if "raw_output" in raw_json_response:
            try:
                # Try to parse the raw_output field
                import re
                json_match = re.search(r'\{.*\}', raw_json_response, re.DOTALL)
                if json_match:
                    potential_json = json_match.group()
                    potential_json = clean_json_response(potential_json)
                    persona_json = json.loads(potential_json)
                else:
                    raise ValueError("No JSON found in response")
            except:
                persona_json = {
                    "error": "Failed to parse JSON from model output.",
                    "raw_output": raw_json_response
                }
        else:
            persona_json = {
                "error": "Failed to parse JSON from model output.",
                "raw_output": raw_json_response
            }

    return persona_text, persona_json