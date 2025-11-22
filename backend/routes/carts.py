from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from ..models import Cart, Item, User
from ..database import get_db
from ..security import get_current_user

router = APIRouter(prefix="/api", tags=["Carrinhos"])

class CartCreate(BaseModel):
    name: str

class ItemCreate(BaseModel):
    name: str

class BulkItems(BaseModel):
    items: list[str]

@router.post("/carrinhos")
def create_cart(cart: CartCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    new_cart = Cart(name=cart.name, user_id=current_user.id)
    db.add(new_cart)
    db.commit()
    db.refresh(new_cart)
    return {"id": new_cart.id, "name": new_cart.name}

@router.get("/carrinhos")
def list_carts(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    carts = db.query(Cart).filter_by(user_id=current_user.id).all()
    return [{"id": c.id, "name": c.name, "status": c.status} for c in carts]

@router.delete("/carrinhos/{cart_id}")
def delete_cart(cart_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    cart = db.query(Cart).filter_by(id=cart_id, user_id=current_user.id).first()
    if not cart:
        raise HTTPException(status_code=404, detail="Carrinho não encontrado")
    db.delete(cart)
    db.commit()
    return {"success": True}

@router.post("/carrinhos/{cart_id}/itens")
def add_item(cart_id: int, item: ItemCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    cart = db.query(Cart).filter_by(id=cart_id, user_id=current_user.id).first()
    if not cart:
        raise HTTPException(status_code=404, detail="Carrinho não encontrado")
    new_item = Item(name=item.name, cart_id=cart.id)
    db.add(new_item)
    db.commit()
    db.refresh(new_item)
    return {"id": new_item.id, "name": new_item.name}

@router.get("/carrinhos/{cart_id}/itens")
def get_cart_items(cart_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    cart = db.query(Cart).filter_by(id=cart_id, user_id=current_user.id).first()
    if not cart:
        raise HTTPException(status_code=404, detail="Carrinho não encontrado")
    items = db.query(Item).filter_by(cart_id=cart.id).all()
    return [{"id": item.id, "name": item.name} for item in items]

@router.delete("/itens/{item_id}")
def delete_item(item_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    item = db.query(Item).join(Cart).filter(Item.id == item_id, Cart.user_id == current_user.id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item não encontrado")
    db.delete(item)
    db.commit()
    return {"success": True}

@router.post("/carrinhos/{cart_id}/bulk")
def add_bulk(cart_id: int, bulk: BulkItems, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    cart = db.query(Cart).filter_by(id=cart_id, user_id=current_user.id).first()
    if not cart:
        raise HTTPException(status_code=404, detail="Carrinho não encontrado")
    for name in bulk.items:
        if name.strip():
            db.add(Item(name=name.strip(), cart_id=cart.id))
    db.commit()
    return {"success": True, "added": bulk.items}