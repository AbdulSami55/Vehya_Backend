from fastapi import APIRouter, Depends, HTTPException, UploadFile,File,status
from fastapi.responses import FileResponse
from ..Users import schemas, crud
from sqlalchemy.orm import Session
import models
from database import SessionLocal, engine, get_db
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")



models.Base.metadata.create_all(bind=engine)

router = APIRouter(
    prefix="/User",
    tags=["User"],
)

@router.post('/SignUp')
async def SignUp(user:schemas.User,db: Session = Depends(get_db)):
    try:
        verify = crud.getUser(db=db, user=user)
        if (verify==None):
            return crud.createUser(db=db, user=user)
        else:
            return HTTPException(detail= 'This User already Exists',status_code=status.HTTP_406_NOT_ACCEPTABLE)
    except:
        return HTTPException(detail="Something Went Wrong",status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.post('/Login-User')
async def Login(user:schemas.User,db: Session = Depends(get_db)):
    try:
        verify = crud.getUser(db=db, user=user)
        if pwd_context.verify(user.password, verify.Password):
            return {
                    'detail':{'Email':verify.Email,
                            'Password':verify.Password,
                            'Id':verify.id}
                    }
        else:
            return HTTPException(detail= 'Incorrect Credentials Entered. Try Again',status_code=status.HTTP_404_NOT_FOUND)
    except:
        return HTTPException(detail="Something Went Wrong",status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)