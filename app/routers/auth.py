from fastapi import HTTPException, status, Depends, APIRouter
from sqlalchemy.orm import Session
from app.database import get_db
from app import models, schemas, utils, oauth2

router = APIRouter(
    prefix='/auth',
    tags=['Authentication']
)


@router.post("/login", response_model=schemas.Token)
async def login(user_credentials: schemas.UserLogin, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == user_credentials.email).first()
    if not user:   
        raise HTTPException(detail="invalid credentials", status_code=status.HTTP_403_FORBIDDEN_)
    
    if not utils.verify(user_credentials.password, user.password):   
        raise HTTPException(detail="invalid credentials", status_code=status.HTTP_403_FORBIDDEN)
    
    access_token = oauth2.create_access_token(data={"user_id": user.id})
    return {"access_token": access_token, "token_type": "bearer"}