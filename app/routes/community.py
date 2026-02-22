from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from ..database import get_db
from .. import models

# Initialize the router
router = APIRouter(prefix="/community", tags=["Community & Leaderboard"])

# --- LEADERBOARD SECTION ---

@router.get("/leaderboard")
def get_leaderboard(db: Session = Depends(get_db)):
    """
    Returns the top 10 students ranked by their InCoScore.
    """
    top_students = (
        db.query(models.User)
        .order_by(models.User.incoscore.desc())
        .limit(10)
        .all()
    )
    return top_students

# --- SOCIAL FEED SECTION ---

@router.get("/posts")
def get_all_posts(db: Session = Depends(get_db)):
    """
    Fetches all academic posts from the community.
    Note: You'll need a 'Post' model in models.py for this to work.
    """
    # Assuming you add a Post model later
    # return db.query(models.Post).order_by(models.Post.created_at.desc()).all()
    return {"message": "Social feed logic ready. Connect to Post model next."}

@router.post("/create-post")
def create_post(user_id: int, content: str, db: Session = Depends(get_db)):
    """
    Allows a student to share an achievement or update.
    """
    # Placeholder for post creation logic
    return {"status": "Post shared successfully", "content": content}