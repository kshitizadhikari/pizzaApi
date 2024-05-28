import uvicorn
from fastapi import FastAPI
from auth_router import auth_router
from order_router import order_router

app = FastAPI(debug=True)
app.include_router(order_router)
app.include_router(auth_router)

@app.get("/")
def index():
    return {
        "data": "This is the starting point"
    }
