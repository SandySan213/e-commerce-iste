from dotenv import load_dotenv
import sys
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import logging
from products.products_api import prod_api
from carts.carts_api import cart_api

load_dotenv()

sys.path.append(os.getenv('project_path'))  # Adding folder path to access files from other directories

app = FastAPI(
    title='Sandy APIs for Personal Use',
    version="1.0.0",
    description="APIs for handling products and carts.",
    swagger_ui_parameters={"defaultModelsExpandDepth": -1}
)

# CORS settings
origins = [
    "http://localhost:4200"
]

app.include_router(prod_api)  # Adding product APIs
app.include_router(cart_api)  # Adding cart APIs

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

# Simple greeting endpoint
@app.get('/', include_in_schema=False)
async def greet():
    return "Welcome to my API!"

if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=3000, log_level=logging.DEBUG)
