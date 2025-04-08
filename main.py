from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import requests
from bs4 import BeautifulSoup
import os
from dotenv import load_dotenv
import json
from datetime import datetime

# Load environment variables
load_dotenv()

app = FastAPI(title="Zureo Integration API")

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Models
class LoginRequest(BaseModel):
    username: str
    password: str

class ZureoSession:
    def __init__(self):
        self.session = requests.Session()
        self.is_logged_in = False
        self.base_url = "https://go.zureo.com"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }

    def login(self, username: str, password: str):
        try:
            # First get the login page to get any necessary tokens
            login_page = self.session.get(f"{self.base_url}/", headers=self.headers)
            soup = BeautifulSoup(login_page.text, 'html.parser')
            
            # Prepare login data
            login_data = {
                "empresaLogin": os.getenv("ZUREO_CODIGO"),
                "usuarioLogin": username,
                "passwordLogin": password
            }
            
            # Perform login
            login_response = self.session.post(
                f"{self.base_url}/api/auth/login",
                json=login_data,
                headers=self.headers
            )
            
            if login_response.status_code == 200:
                self.is_logged_in = True
                return {"status": "success", "message": "Login successful"}
            else:
                raise HTTPException(status_code=401, detail="Invalid credentials")
                
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    def get_stock(self, sku: str):
        if not self.is_logged_in:
            raise HTTPException(status_code=401, detail="Not logged in")
            
        try:
            # Get stock page
            stock_url = f"{this.base_url}/api/stock/articulo/{sku}"
            response = self.session.get(stock_url, headers=self.headers)
            
            if response.status_code == 200:
                data = response.json()
                return {"sku": sku, "stock": data.get("stock", 0)}
            else:
                raise HTTPException(status_code=404, detail="Stock not found")
                
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    def adjust_stock(self, sku: str, cantidad: int):
        if not self.is_logged_in:
            raise HTTPException(status_code=401, detail="Not logged in")
            
        try:
            # Prepare adjustment data
            adjustment_data = {
                "sku": sku,
                "cantidad": cantidad,
                "tipo": "ajuste"
            }
            
            # Send adjustment request
            adjust_url = f"{this.base_url}/api/stock/ajustar"
            response = self.session.post(
                adjust_url,
                json=adjustment_data,
                headers=self.headers
            )
            
            if response.status_code == 200:
                return {"success": True, "message": f"Stock adjusted to {cantidad} for SKU {sku}"}
            else:
                raise HTTPException(status_code=400, detail="Failed to adjust stock")
                
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

# Create a global session instance
zureo_session = ZureoSession()

# Health check endpoint
@app.get("/")
async def health_check():
    return {
        "status": "UP",
        "timestamp": datetime.now().isoformat(),
        "service": "Zureo Integration API",
        "version": "1.0.0",
        "endpoints": {
            "login": "/zureo/login",
            "stock": "/zureo/stock/{sku}",
            "adjust": "/zureo/ajustar/{sku}/{cantidad}"
        }
    }

# Login endpoint
@app.post("/zureo/login")
async def login(login_data: LoginRequest):
    return zureo_session.login(login_data.username, login_data.password)

# Stock check endpoint
@app.get("/zureo/stock/{sku}")
async def get_stock(sku: str):
    return zureo_session.get_stock(sku)

# Stock adjustment endpoint
@app.get("/zureo/ajustar/{sku}/{cantidad}")
async def adjust_stock(sku: str, cantidad: int):
    return zureo_session.adjust_stock(sku, cantidad)

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port) 