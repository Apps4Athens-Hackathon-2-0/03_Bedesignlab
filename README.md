# 03_Bedesignlab
# News Story Generator

AI-powered interactive storytelling based on daily news.

## Features
- Generates stories from today's top news headlines
- Interactive choice-based narrative
- Automatic story conclusion after 4 choices
- Powered by Claude AI

## Setup Instructions

### Backend Setup

1. Navigate to backend folder:
```bash
cd backend
```

2. Create virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create `.env` file with your API keys:
```
ANTHROPIC_API_KEY=your_key_here
NEWS_API_KEY=your_key_here
```

5. Run the backend:
```bash
uvicorn main:app --reload
```

### Frontend Setup

1. Navigate to frontend folder:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Start the development server:
```bash
npm start
```

4. Open http://localhost:3000

## Tech Stack

**Backend:**
- Python 3.10+
- FastAPI
- SQLAlchemy
- Anthropic Claude API
- NewsAPI

**Frontend:**
- React
- Axios
- CSS3

## API Keys Required

- **Anthropic API**: https://console.anthropic.com/
- **NewsAPI**: https://newsapi.org/register

## Project Structure
```
news-story-app/
├── backend/
│   ├── main.py
│   ├── ai_service.py
│   ├── news_service.py
│   ├── database.py
│   ├── requirements.txt
│   └── .env (not in git)
├── frontend/
│   ├── src/
│   │   ├── App.js
│   │   └── App.css
│   └── package.json
└── README.md
```

## License
MIT