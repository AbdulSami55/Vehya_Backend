from fastapi import HTTPException
from ..FeaturedProducts import schemas
import models
from fastapi import status
from sqlalchemy.orm import Session


def checkProduct(product:schemas.FeaturedProduct, db:Session):
    try:
        check_product = db.query(models.FeaturedProducts).filter(models.FeaturedProducts.ProductID==product.ProductID,models.FeaturedProducts.Category==product.Category).first()
        if check_product:
            return True
        else:
            return False
    except:
        return HTTPException(detail='Something went wrong', status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
def checkProductbyCategory(product:schemas.FeaturedProduct, db:Session):
    try:
        check_product = db.query(models.FeaturedProducts).filter(models.FeaturedProducts.Category==product.Category).first()
        if check_product:
            return True
        else:
            return False
    except:
        return HTTPException(detail='Something went wrong', status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    

def checkProductbyId(Id:int, db:Session):
    try:
        check_product = db.query(models.FeaturedProducts).filter(models.FeaturedProducts.id==Id).first()
        if check_product:
            return True
        else:
            return False
    except:
        return HTTPException(detail='Something went wrong', status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)