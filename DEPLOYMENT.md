# 🚀 Deployment Guide

## Koyeb Deployment Steps

### 1. Repository Setup
```bash
git add .
git commit -m "Ready for deployment"
git push origin main
```

### 2. Koyeb Configuration

#### Build Settings:
- **Build Command**: Leave empty (auto-detect) OR use `pip3 install -r requirements.txt`
- **Run Command**: `python3 start.py`
- **Port**: Auto-detected from `$PORT` environment variable

#### Environment Variables:
Set these in Koyeb dashboard:
```
REDDIT_CLIENT_ID=your_reddit_client_id
REDDIT_CLIENT_SECRET=your_reddit_client_secret
REDDIT_CLIENT_AGENT=script:PersonaBuilder:v1.0 (by u/yourusername)
GROQ_API_KEY=your_groq_api_key
```

### 3. Alternative Build Commands (if pip not found)

Try these build commands in order:

#### Option 1: Auto-detect (Recommended)
```
# Leave build command empty
```

#### Option 2: Explicit pip3
```
pip3 install -r requirements.txt
```

#### Option 3: Python module
```
python3 -m pip install -r requirements.txt
```

#### Option 4: With upgrade
```
python3 -m pip install --upgrade pip && pip3 install -r requirements.txt
```

### 4. Alternative Procfile Options

If `python3 start.py` doesn't work, try updating Procfile to:

#### Option A: Direct Flask
```
web: python3 app.py
```

#### Option B: With module
```
web: python3 -m flask run --host=0.0.0.0 --port=$PORT
```

#### Option C: Gunicorn (install first)
```
web: pip3 install gunicorn && python3 -m gunicorn app:app --bind 0.0.0.0:$PORT
```

## Troubleshooting Common Issues

### Build Fails with Exit Code 51
**Possible causes:**
1. Python version incompatibility
2. Missing dependencies
3. Import errors

**Solutions:**
1. Remove `runtime.txt` (let platform auto-detect Python)
2. Simplify `requirements.txt` to only essential packages
3. Check that all imports work locally

### Environment Variables Not Found
**Check:**
1. All 4 required variables are set in Koyeb dashboard
2. Variable names match exactly (case-sensitive)
3. No extra spaces in variable values

### Import Errors
**Ensure:**
1. All Python files are in the repository
2. No missing dependencies in `requirements.txt`
3. File paths are correct

## Testing Deployment

### Health Check
Once deployed, visit: `https://your-app.koyeb.app/health`

Should return:
```json
{
  "status": "healthy",
  "message": "Reddit Persona Generator is running",
  "debug": false
}
```

### Full Test
1. Visit your app URL
2. Enter a Reddit username (e.g., "kojied")
3. Click "Analyze Profile"
4. Verify persona generation works
5. Test download functionality

## Production Notes

- File storage is disabled in production
- No persona history feature
- All data is processed in real-time
- Downloads work from memory, not saved files