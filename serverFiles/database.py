from motor.motor_asyncio import AsyncIOMotorClient
import os

connection_string = os.getenv('db_url')

client = AsyncIOMotorClient(connection_string)

learning_db = client.get_database('learning')

PROD_COL = learning_db.get_collection('products')

CARTS = learning_db.get_collection('product_carts')
