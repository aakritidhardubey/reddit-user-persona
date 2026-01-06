from flask import Flask, request, jsonify, render_template, send_from_directory
from flask_cors import CORS
import os
import json
from reddit_scraper import scrape_user
from groq_llm import generate_persona

app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/generate-persona', methods=['POST'])
def generate_persona_api():
    try:
        data = request.get_json()
        username = data.get('username', '').strip()
        
        if not username:
            return jsonify({'error': 'Username is required'}), 400
        
        # Remove u/ or r/ prefix if present
        if username.startswith(('u/', 'r/')):
            username = username[2:]
        
        print(f"🔍 Generating persona for u/{username}...")
        posts, comments = scrape_user(username)
        
        if not posts and not comments:
            return jsonify({'error': 'No data found or user doesn\'t exist'}), 404
        
        persona_text, persona_json = generate_persona(posts, comments)
        
        # For production deployment, we'll store in memory/session instead of files
        # Only save files in development mode
        if app.debug:
            # Save files in development
            output_dir = "output"
            os.makedirs(output_dir, exist_ok=True)
            
            with open(f"output/{username}_persona.txt", "w", encoding="utf-8") as f:
                f.write(persona_text)
            
            with open(f"output/{username}_persona.json", "w", encoding="utf-8") as jf:
                json.dump(persona_json, jf, indent=4, ensure_ascii=False)
        
        return jsonify({
            'success': True,
            'username': username,
            'persona_text': persona_text,
            'persona_json': persona_json
        })
        
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/personas')
def list_personas():
    try:
        # In production, we don't have persistent storage
        # So we'll return empty list for now
        if not app.debug:
            return jsonify({'personas': []})
            
        output_dir = "output"
        if not os.path.exists(output_dir):
            return jsonify({'personas': []})
        
        personas = []
        for filename in os.listdir(output_dir):
            if filename.endswith('_persona.json'):
                username = filename.replace('_persona.json', '')
                personas.append(username)
        
        return jsonify({'personas': personas})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/persona/<username>')
def get_persona(username):
    try:
        # In production, we don't have persistent storage
        if not app.debug:
            return jsonify({'error': 'Persona history not available in production'}), 404
            
        json_path = f"output/{username}_persona.json"
        txt_path = f"output/{username}_persona.txt"
        
        if not os.path.exists(json_path):
            return jsonify({'error': 'Persona not found'}), 404
        
        with open(json_path, 'r', encoding='utf-8') as f:
            persona_json = json.load(f)
        
        persona_text = ""
        if os.path.exists(txt_path):
            with open(txt_path, 'r', encoding='utf-8') as f:
                persona_text = f.read()
        
        return jsonify({
            'username': username,
            'persona_json': persona_json,
            'persona_text': persona_text
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=False, host='0.0.0.0', port=port)