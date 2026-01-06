import os
import json
import requests
from dotenv import load_dotenv

load_dotenv()

def make_groq_request(messages, model="llama-3.3-70b-versatile", temperature=0.7):
    """Make a direct HTTP request to Groq API"""
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise ValueError("GROQ_API_KEY not found in environment variables")
    
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    data = {
        "model": model,
        "messages": messages,
        "temperature": temperature
    }
    
    response = requests.post(url, headers=headers, json=data)
    response.raise_for_status()
    
    return response.json()

def generate_prompt(posts, comments):
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

def generate_persona(posts, comments):
    try:
        prompt = generate_prompt(posts, comments)
        
        # Generate text persona
        response = make_groq_request([
            {"role": "user", "content": prompt}
        ], temperature=0.7)
        
        persona_text = response['choices'][0]['message']['content'].strip()
        
        # Generate structured JSON
        struct_prompt = generate_structured_prompt(persona_text)
        struct_response = make_groq_request([
            {"role": "user", "content": struct_prompt}
        ], temperature=0.3)
        
        raw_json_response = struct_response['choices'][0]['message']['content']
        cleaned_json = clean_json_response(raw_json_response)
        
        try:
            persona_json = json.loads(cleaned_json)
        except json.JSONDecodeError as e:
            print(f"JSON Parse Error: {e}")
            print(f"Raw response: {raw_json_response}")
            print(f"Cleaned response: {cleaned_json}")
            
            persona_json = {
                "error": "Failed to parse JSON from model output.",
                "raw_output": raw_json_response
            }
        
        return persona_text, persona_json
        
    except Exception as e:
        print(f"Error in generate_persona: {e}")
        return f"Error generating persona: {str(e)}", {"error": str(e)}