from dotenv import load_dotenv
import sys
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from products.products_api import prod_api


load_dotenv()

sys.path.append(os.getenv('project_path')) # #adding folder path to access files from other directories


app = FastAPI(title='sandy apis for personal use',
              swagger_ui_parameters={"defaultModelsExpandDepth": -1})

# handled CORS here

app.add_middleware(CORSMiddleware,
    allow_credentials=True,
    allow_origins=['*'],
    allow_methods=['*'],
    allow_headers=['*']
)

app.include_router(prod_api) # adding product apis

 
@app.get('/', include_in_schema=False) # simple greet
async def greet():
    return "Welcome to my stupid api!."


if __name__=='__main__':
    uvicorn.run(app)
