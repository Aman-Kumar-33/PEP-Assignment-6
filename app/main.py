import os
from pathlib import Path
from fastapi import FastAPI, Depends, BackgroundTasks, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

# Internal Imports
from .database import engine, get_db
from . import models
from .routes import auth, community
from .services.scraper import scrape_ivy_opportunities
from .services.classifier import classify_opportunity

# --- PATH LOGIC (Fixes the "Directory does not exist" error) ---
# This finds the absolute path to your 'app' folder
BASE_DIR = Path(__file__).resolve().parent

# --- DATABASE INIT ---
# Creates tables in MySQL based on your models.py
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Ivy League Intelligence Network")

# --- STATIC FILES ---
# This looks specifically for D:\LPU\pep\Assignments\6\app\static
static_dir = BASE_DIR / "static"
if not static_dir.exists():
    os.makedirs(static_dir) # Creates it if you forgot

app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")

# --- INCLUDE ROUTES ---
app.include_router(auth.router)
app.include_router(community.router)

# --- WEB ROUTES ---

@app.get("/dashboard")
def get_dashboard():
    """Serves the dashboard HTML file from app/templates/"""
    template_path = BASE_DIR / "templates" / "dashboard.html"
    if not template_path.exists():
        return {"error": f"File not found at {template_path}. Please create the file!"}
    return FileResponse(str(template_path))

@app.get("/")
def home():
    # This now serves the main aggregator as the first thing users see
    return FileResponse("app/templates/index.html")

# --- OPPORTUNITY LOGIC ---

from .services.scraper import scrape_ivy_opportunities # Update the import name

@app.get("/scrape-now")
def trigger_scrape(db: Session = Depends(get_db)):
    # Update this line to the new function name
    data = scrape_ivy_opportunities() 
    # ... rest of the code ... # Call the new multi-scraper
    new_count = 0
    
    for item in data:
        # Check link for duplicates
        exists = db.query(models.Opportunity).filter(models.Opportunity.link == item['link']).first()
        
        if not exists:
            print(f"NEW FOUND: {item['title']}")
            # AI Classification
            item['domain'] = classify_opportunity(item['title'])
            
            new_opp = models.Opportunity(**item)
            db.add(new_opp)
            new_count += 1
        else:
            print(f"SKIPPED (Duplicate): {item['title']}")
            
    db.commit()
    return {"status": "Success", "scraped": len(data), "new_added": new_count}

@app.get("/opportunities")
def list_opportunities(db: Session = Depends(get_db)):
    """API endpoint for the frontend to get all opportunities."""
    return db.query(models.Opportunity).order_by(models.Opportunity.created_at.desc()).all()
@app.get("/notifications/{user_interest}")
def get_notifications(user_interest: str, db: Session = Depends(get_db)):
    # Find opportunities where the AI domain matches the student's interest
    matches = db.query(models.Opportunity).filter(
        models.Opportunity.domain.ilike(f"%{user_interest}%")
    ).all()
    return matches

@app.post("/apply/{opp_id}")
def apply_to_opportunity(opp_id: int, user_id: int, db: Session = Depends(get_db)):
    # 1. Verify the opportunity exists
    opportunity = db.query(models.Opportunity).filter(models.Opportunity.id == opp_id).first()
    if not opportunity:
        raise HTTPException(status_code=404, detail="Opportunity not found")
    
    # 2. Record the application
    new_app = models.Application(user_id=user_id, opportunity_id=opp_id)
    db.add(new_app)
    db.commit()
    
    return {"message": f"Application for {opportunity.title} recorded successfully!"}