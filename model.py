from sqlalchemy import Column, String, DateTime
from datetime import datetime
from database import Base


class ShopStatus(Base):
    __tablename__ = "shop_status"

    shop_code = Column(String, primary_key=True, index=True)
    shop_name = Column(String)
    status = Column(String)
    last_transaction = Column(String)
    updated_at = Column(DateTime, default=datetime.utcnow)