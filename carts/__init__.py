from fastapi import APIRouter, HTTPException, status
from serverFiles.database import PROD_COL, CARTS
from serverFiles import schemas
from bson import ObjectId
from typing import List