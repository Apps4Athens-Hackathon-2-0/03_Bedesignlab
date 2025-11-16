from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sqlalchemy.orm import Session
import json

from database import get_db, Story
from news_service import fetch_top_news
from ai_service import generate_initial_story, continue_story

app = FastAPI()

# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request models
class ContinueRequest(BaseModel):
    story_id: int
    user_input: str

# Routes
@app.get("/")
def read_root():
    return {"message": "News Story Generator API"}

@app.post("/api/generate-story")
def create_story(db: Session = Depends(get_db)):
    """Generate initial story from today's news"""
    
    # Step 1: Fetch news
    news_summary = fetch_top_news()
    
    # Step 2: Generate story
    initial_story = generate_initial_story(news_summary)
    
    # Step 3: Store in database
    conversation_history = [
        {"role": "system", "content": "You are a creative storyteller who creates engaging fiction based on real news."},
        {"role": "assistant", "content": initial_story}
    ]
    
    db_story = Story(
        news_summary=news_summary,
        initial_story=initial_story,
        conversation_history=json.dumps(conversation_history)
    )
    db.add(db_story)
    db.commit()
    db.refresh(db_story)
    
    return {
        "story_id": db_story.id,
        "news_summary": news_summary,
        "story": initial_story
    }

@app.post("/api/continue-story")
def continue_story_endpoint(request: ContinueRequest, db: Session = Depends(get_db)):
    """Continue the story based on user input"""
    
    # Get story from database
    story = db.query(Story).filter(Story.id == request.story_id).first()
    if not story:
        raise HTTPException(status_code=404, detail="Story not found")
    
    # Load conversation history
    conversation_history = json.loads(story.conversation_history)
    
    # Generate continuation
    continuation = continue_story(conversation_history, request.user_input)
    
    # Update conversation history
    conversation_history.append({"role": "user", "content": request.user_input})
    conversation_history.append({"role": "assistant", "content": continuation})
    
    story.conversation_history = json.dumps(conversation_history)
    db.commit()
    
    return {
        "story_id": story.id,
        "continuation": continuation
    }

@app.get("/api/story/{story_id}")
def get_story(story_id: int, db: Session = Depends(get_db)):
    """Get a story by ID"""
    story = db.query(Story).filter(Story.id == story_id).first()
    if not story:
        raise HTTPException(status_code=404, detail="Story not found")
    
    return {
        "story_id": story.id,
        "news_summary": story.news_summary,
        "initial_story": story.initial_story,
        "created_at": story.created_at
    }