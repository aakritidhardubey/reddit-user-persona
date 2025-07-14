import os
import praw
import json 
from dotenv import load_dotenv
# llm
from groq_llm import generate_persona

load_dotenv()

reddit=praw.Reddit(
    client_id=os.getenv("REDDIT_CLIENT_ID"),
    client_secret=os.getenv("REDDIT_CLIENT_SECRET"),
    user_agent=os.getenv("REDDIT_CLIENT_AGENT")
)

def scrape_user(username):
    user=reddit.redditor(username)
    posts=[]
    comments=[]

    try:
        for submission in user.submissions.new(limit=50):
            posts.append(f"Title: {submission.title}\n Text: {submission.selftext}")
        for comment in user.comments.new(limit=50):
            comments.append(comment.body)
    except Exception as e:
        print("Error: ",e)
    
    return posts,comments

if __name__ == "__main__":
    while True:
        username = input("Enter the Reddit username (without r/ or u/)(or type 'exit' to quit): ").strip()

        if username.lower()=="exit":
            break

        print(f"\n🔍 Generating persona for u/{username}...")
        posts, comments = scrape_user(username)

        if not posts and not comments:
            print("No data found or user doesn't exist.")
        else:
            persona_text,persona_json = generate_persona(posts, comments)

            output_dir="output"
            os.makedirs(output_dir,exist_ok=True)

            with open(f"output/{username}_persona.txt", "w", encoding="utf-8") as f:
                f.write(persona_text)

            with open(f"output/{username}_persona.json", "w", encoding="utf-8") as jf:
                json.dump(persona_json,jf,indent=4,ensure_ascii=False)

            print(f"Persona saved ")
