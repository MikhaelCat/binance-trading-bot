from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
import uvicorn
from config.settings import settings

app = FastAPI(title="Binance Trading Bot", version="1.0.0")

# Подключение статических файлов и шаблонов
app.mount("/static", StaticFiles(directory="web/static"), name="static")
templates = Jinja2Templates(directory="web/templates")

# Подключение роутов
from web.routes import dashboard, trades, api
app.include_router(dashboard.router)
app.include_router(trades.router)
app.include_router(api.router)

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("dashboard.html", {"request": request})

if __name__ == "__main__":
    uvicorn.run(
        "web.app:app",
        host=settings.WEB_HOST,
        port=settings.WEB_PORT,
        reload=True
    )