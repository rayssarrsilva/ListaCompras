from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from models import Cart, Item
from database import get_db

router = APIRouter(prefix="/api", tags=["Carrinhos"])

@router.get("/carrinhos/{cart_id}/itens")
def get_cart_items(cart_id: int, db: Session = Depends(get_db)):
    cart = db.query(Cart).filter_by(id=cart_id).first()
    if not cart:
        raise HTTPException(status_code=404, detail="Carrinho não encontrado")
    items = db.query(Item).filter_by(cart_id=cart.id).all()
    return [{"id": item.id, "name": item.name} for item in items]

@router.delete("/itens/{item_id}")
def delete_item(item_id: int, db: Session = Depends(get_db)):
    item = db.query(Item).filter_by(id=item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item não encontrado")
    db.delete(item)
    db.commit()
    return {"success": True}
