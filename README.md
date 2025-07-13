# 🧠 Reddit User Persona Generator

This project generates detailed **user personas** based on public Reddit profiles using a combination of **Reddit API** and **Groq's LLaMA-3 LLM**. The script scrapes posts and comments from a user and analyzes them to extract personality, interests, demographics, career indicators, and more.

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
REDDIT_USER_AGENT=script:PersonaBuilder:v1.0 (by u/yourusername)
GROQ_API_KEY=your_groq_api_key
```

⚠️ **Important**: Do not commit your `.env` file to GitHub.

---

## 🚀 How to Run

```bash
python reddit_scraper.py
```

The script will:

1. Scrape Reddit data for each user listed
2. Generate both `.txt` and `.json` persona files
3. Save them in the `output/` directory

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

- Python 3.11+
- Reddit API with PRAW
- Groq LLaMA-3 API
- dotenv, openai, json

---

## 🚧 Future Improvements

| Feature | Description |
|---------|-------------|
| 🔍 Search UI | Build Streamlit UI to enter any Reddit profile |
| 📊 Dashboard | View multiple personas visually |
| 💬 LLM Comparisons | Try GPT-4, Claude, Mistral, etc. |
| 🗃️ Data Persistence | Store outputs in MongoDB or SQLite |
| 🧠 Topic Extraction | NLP-based topic and summary generation |
| 📤 CSV Export | Export to Excel/Power BI/Google Sheets |

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