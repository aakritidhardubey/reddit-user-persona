# 🧠 Reddit User Persona Generator

This project generates detailed **user personas** based on public Reddit profiles using a combination of **Reddit API** and **Groq's LLaMA-3 LLM**. The script scrapes posts and comments from a user and analyzes them to extract personality, interests, demographics, career indicators, and more.
It's Deployed now , check it at:- [reddit-persona](https://imaginative-jane-aakritidubey21-5e1aa5fc.koyeb.app/)

---

## 📌 Sample Profiles

This repository includes personas generated for:

- [u/kojied](https://www.reddit.com/user/kojied)
- [u/Hungry-Move-6603](https://www.reddit.com/user/Hungry-Move-6603)

You'll find both `.txt` and `.json` personas for each in the `output/` folder.

---

## ✨ Features

- 🔍 Scrapes posts and comments from Reddit users  
- 🤖 Uses **LLaMA-3** via **Groq API** to analyze behavior  
- 📄 Outputs human-readable `.txt` files  
- 📦 Also saves structured `.json` files  
- 📚 Each persona includes citations from the user's own content  

---

## ⚙️ Setup Instructions

### 1. Clone the Repository
```bash
git clone https://github.com/your-username/reddit-user-persona-generator.git
cd reddit-user-persona-generator
```

### 2. Set Up Virtual Environment

```bash
python -m venv venv
venv\Scripts\activate     # On Windows
# or
source venv/bin/activate  # On Mac/Linux
```

### 3. Install Required Libraries
```bash
pip install -r requirements.txt
```

### 4. Create .env File
Create a `.env` file in the root folder and add the following content:

```env
REDDIT_CLIENT_ID=your_reddit_client_id
REDDIT_CLIENT_SECRET=your_reddit_client_secret
REDDIT_CLIENT_AGENT=script:PersonaBuilder:v1.0 (by u/yourusername)
GROQ_API_KEY=your_groq_api_key
```

---

## 🌐 Deployment

### Koyeb Deployment
1. Fork this repository to your GitHub
2. Connect your GitHub account to Koyeb
3. Create a new app and select this repository
4. Set the following environment variables in Koyeb:
   - `REDDIT_CLIENT_ID`
   - `REDDIT_CLIENT_SECRET` 
   - `REDDIT_CLIENT_AGENT`
   - `GROQ_API_KEY`
5. Deploy!

### Other Platforms (Heroku, Railway, etc.)
The app is configured to work with any platform that supports Python web apps:
- Uses `Procfile` for process definition
- Reads `PORT` from environment variables
- Handles production vs development modes automatically

---

## 🚀 How to Run

### 🌐 Web Interface (Recommended)

#### Local Development
```bash
python run_app.py
```

Then open your browser and go to: **http://localhost:5000**

#### Production Deployment (Koyeb/Heroku/etc.)
1. Set environment variables in your deployment platform
2. The app will automatically run in production mode
3. File storage is disabled in production (ephemeral storage)

The web interface provides:
- 🎨 Beautiful, modern UI with gradient backgrounds
- 📊 Visual persona cards with organized information
- 📝 Detailed analysis section with narrative explanation
- 🔄 Real-time generation with animated loading indicators
- 📱 Fully responsive design for mobile and desktop
- 💾 Download options (Text, JSON, PDF)

### 💻 Command Line Interface
```bash
python reddit_scraper.py
```

The script will:

1.Prompt you to enter a Reddit username (e.g., kojied, Hungry-Move-6603)

2.Scrape the user’s public posts and comments

3.Generate a detailed persona using LLM

4.Save the output as both .txt and .json files in the output/ folder

5.Let you continue entering more usernames until you type exit to quit


---

## 📂 Output Files

Each Reddit user will generate:

### 🔹 Text File (.txt)
A human-readable persona with:
- Demographics
- Interests & hobbies
- Personality traits
- Career details
- Technical skills
- Social behavior
- 🔍 With citations from their posts/comments

### 🔹 JSON File (.json)
Structured format suitable for dashboards or automation:

```json
{
  "demographics": {
    "age": "25-35",
    "location": "USA",
    "gender": "Male"
  },
  "interests": ["Gaming", "Technology", "Cooking"],
  "citations": {
    "interests": "I play Elden Ring every weekend."
  }
}
```

---

## 🧠 Technologies Used

### Backend
- Python 3.11+
- Reddit API with PRAW
- Groq LLaMA-3 API
- Flask web framework
- dotenv, openai, json

### Frontend
- HTML5, CSS3, JavaScript (ES6+)
- Modern responsive design with CSS Grid & Flexbox
- Font Awesome icons
- Gradient backgrounds and smooth animations
- RESTful API integration

---

## 🚧 Future Improvements

| Feature | Description | Status |
|---------|-------------|--------|
| ✅ Web UI | Beautiful web interface to enter Reddit profiles | **Completed** |
| ✅ Visual Dashboard | View personas with organized cards and multiple views | **Completed** |
| 💬 LLM Comparisons | Try GPT-4, Claude, Mistral, etc. | Planned |
| 🗃️ Data Persistence | Store outputs in MongoDB or SQLite | Planned |
| 🧠 Topic Extraction | NLP-based topic and summary generation | Planned |
| 📤 CSV Export | Export to Excel/Power BI/Google Sheets | Planned |
| 🔍 Advanced Search | Search through generated personas | Planned |
| 📊 Analytics | Usage statistics and persona insights | Planned |

---

## 👩‍💻 Author

**Aakriti Dhar Dubey**  
📍 Greater Noida | 🎓 B.Tech Student | 💼 AI/ML Enthusiast  
🔗 [GitHub](https://github.com/aakritidhardubey)  
🔗 [LinkedIn](https://linkedin.com/in/aakritidhardubey)

---

## 📜 License

This project is built for evaluation and learning purposes.  
All content is original and will remain the intellectual property of the author unless selected for internship work by BeyondChats.
