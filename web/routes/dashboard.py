from fastapi import APIRouter, Request, Depends, HTMLResponse # <-- Добавлен HTMLResponse
from fastapi.templating import Jinja2Templates
from database.database import get_db
from sqlalchemy.orm import Session
from database.models import Trade, Signal

router = APIRouter(prefix="", tags=["dashboard"])
templates = Jinja2Templates(directory="web/templates")

@router.get("/dashboard", response_class=HTMLResponse) # <-- HTMLResponse теперь определен
async def dashboard(request: Request, db: Session = Depends(get_db)):
    # Получение последних сделок
    recent_trades = db.query(Trade).order_by(Trade.timestamp.desc()).limit(10).all()
    
    # Получение последних сигналов
    recent_signals = db.query(Signal).order_by(Signal.timestamp.desc()).limit(10).all()
    
    return templates.TemplateResponse("dashboard.html", {
        "request": request,
        "trades": recent_trades,
        "signals": recent_signals
    })
