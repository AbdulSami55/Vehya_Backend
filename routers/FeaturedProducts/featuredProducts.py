import os
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, UploadFile,File,status
from fastapi.responses import FileResponse
from ..FeaturedProducts import schemas, crud
from sqlalchemy.orm import Session
import models
from database import SessionLocal, engine, get_db
import shutil

models.Base.metadata.create_all(bind=engine)

router = APIRouter(
    prefix="/Featured-Products",
    tags=["Featured-Products"],
)

@router.post('/Add-Featured_product')
def AddFeaturedProduct(Product:schemas.FeaturedProduct, db: Session = Depends(get_db) ):
    try:
        check_product = crud.checkProduct(db=db, product=Product)
        check_product_by_category = crud.checkProductbyCategory(db=db, product=Product)

        if check_product ==True:
            return {'Message':'Product Already Exists'}
        if check_product_by_category == True:
            return {'Message':'Product category Already Exists'}
        else:
            product = models.FeaturedProducts(ProductID=Product.ProductID,Category=Product.Category )
            db.add(product)
            db.commit()
            db.refresh(product)
            return {'Message':'Product Successfully Added'}
       
    except:
        return HTTPException(detail='Something went Wrong', status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

@router.delete('/Delete-Featured_product')    
def DeleteFeaturedProduct(Id:int,db: Session = Depends(get_db)):
    try:
        check_product = crud.checkProductbyId(db=db, Id=Id)
        if check_product ==True:
            getProduct = db.query(models.FeaturedProducts).filter(models.FeaturedProducts.id==Id)
            getProduct.delete(synchronize_session=False)
            db.commit()
            return {'Message':'Deleted Successfully'}
        else:
            return {'Message':'Does not Exist'}

    except: 
        return HTTPException(detail='Something went wrong', status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
@router.get('/Get-Featured_product')    
async def getFeaturedProduct(db: Session = Depends(get_db)):
    try:
        # end_index = 1000000000
        total_rows = db.query(models.FeaturedProducts).count()
        Products =  db.query(models.FeaturedProducts).slice(start=0, stop=total_rows).all()
        return {'Products':Products,
                'Total':total_rows}

    except:
        return HTTPException(detail='Something went wrong', status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    

@router.get('/Get-Featured_product-By-Category')    
async def getFeaturedProductbyCategory(Category:str,db: Session = Depends(get_db)):
    try:
        # end_index = 1000000000
        Product =  db.query(models.FeaturedProducts).filter(models.FeaturedProducts.Category==Category).first()
        
    
        return {'ProductsID':Product.ProductID}

    except:
        return HTTPException(detail='Something went wrong', status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)