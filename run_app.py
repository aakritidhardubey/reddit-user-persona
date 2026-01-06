#!/usr/bin/env python3
"""
Simple script to run the Reddit User Persona Generator web app
"""

import os
import sys
from app import app

def check_env_file():
    """Check if .env file exists and has required variables"""
    if not os.path.exists('.env'):
        print("❌ .env file not found!")
        print("Please create a .env file with the following variables:")
        print("REDDIT_CLIENT_ID=your_reddit_client_id")
        print("REDDIT_CLIENT_SECRET=your_reddit_client_secret")
        print("REDDIT_CLIENT_AGENT=script:PersonaBuilder:v1.0 (by u/yourusername)")
        print("GROQ_API_KEY=your_groq_api_key")
        return False
    
    # Check if required variables are set
    from dotenv import load_dotenv
    load_dotenv()
    
    required_vars = ['REDDIT_CLIENT_ID', 'REDDIT_CLIENT_SECRET', 'REDDIT_CLIENT_AGENT', 'GROQ_API_KEY']
    missing_vars = []
    
    for var in required_vars:
        if not os.getenv(var):
            missing_vars.append(var)
    
    if missing_vars:
        print(f"❌ Missing environment variables: {', '.join(missing_vars)}")
        print("Please add them to your .env file")
        return False
    
    return True

if __name__ == '__main__':
    print("🧠 Reddit User Persona Generator")
    print("=" * 40)
    
    # Check environment setup
    if not check_env_file():
        sys.exit(1)
    
    print("✅ Environment variables configured")
    print("🚀 Starting web server...")
    print("📱 Open your browser and go to: http://localhost:5000")
    print("🛑 Press Ctrl+C to stop the server")
    print("=" * 40)
    
    try:
        app.run(debug=True, host='0.0.0.0', port=5000)
    except KeyboardInterrupt:
        print("\n👋 Server stopped. Goodbye!")