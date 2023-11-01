import models
from ..Users import schemas
from fastapi import HTTPException,status
from sqlalchemy.orm import Session
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verifyUser(db:Session, user:schemas.User):
    try:
        User = db.query(models.User).filter(models.User.Email==user.email , models.User.Password == user.password).first()
        if User: 
            return True
        else:
            return False
    except:
        return HTTPException(detail="Something Went Wrong",status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
def getUser(db:Session, user:schemas.User):
    try:
        return db.query(models.User).filter(models.User.Email==user.email).first()
    except:
        return HTTPException(detail="Something Went Wrong",status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


def createUser(db:Session, user:schemas.User):
    try:
        User = models.User(Email=user.email, Password=pwd_context.hash(user.password))
        db.add(User)
        db.commit()
        db.refresh(User)
        return "User Successfully Created"
    except:
        return HTTPException(detail="Something Went Wrong",status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
