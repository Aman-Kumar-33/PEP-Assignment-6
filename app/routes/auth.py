from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from .. import models, schemas
from ..services.incoscore import calculate_incoscore

# THIS IS THE MISSING LINE:
router = APIRouter(prefix="/user", tags=["User Profile"])

@router.put("/update-profile/{user_id}")
def update_profile(user_id: int, research: int, hackathons: int, db: Session = Depends(get_db)):
    # ... rest of your code ...
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Update data
    user.research_papers = research
    user.hackathons_count = hackathons
    
    # Recalculate InCoScore
    user.incoscore = calculate_incoscore(user)
    
    db.commit()
    db.refresh(user)
    return {"message": "Profile Updated", "new_incoscore": user.incoscore}