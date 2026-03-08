from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from test_app import scrape_shop
from sqlalchemy.orm import Session
from database import get_db
from model import ShopStatus
from datetime import datetime

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # allow all origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



@app.get("/shop-status")
def get_shop_status( db: Session = Depends(get_db)):

    shop = db.query(ShopStatus).first()

   
    return {
        "shop_code": shop.shop_code,
        "shop_name": shop.shop_name,
        "status": shop.status,
        "last_transaction": shop.last_transaction,
        "updated_at": shop.updated_at
    }