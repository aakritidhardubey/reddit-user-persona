#!/usr/bin/env python3
"""
Production startup script for Reddit Persona Generator
"""

import os
import sys

def check_environment():
    """Check if all required environment variables are set"""
    required_vars = [
        'REDDIT_CLIENT_ID',
        'REDDIT_CLIENT_SECRET', 
        'REDDIT_CLIENT_AGENT',
        'GROQ_API_KEY'
    ]
    
    missing = []
    for var in required_vars:
        if not os.environ.get(var):
            missing.append(var)
    
    if missing:
        print(f"❌ Missing environment variables: {', '.join(missing)}")
        return False
    
    print("✅ All environment variables are set")
    return True

def main():
    """Main startup function"""
    print("🚀 Starting Reddit Persona Generator...")
    
    if not check_environment():
        sys.exit(1)
    
    # Import and run the Flask app
    try:
        from app import app
        port = int(os.environ.get('PORT', 5000))
        app.run(host='0.0.0.0', port=port, debug=False)
    except Exception as e:
        print(f"❌ Failed to start application: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()