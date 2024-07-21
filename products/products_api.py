from fastapi import APIRouter, HTTPException, status
from serverFiles.database import PROD_COL
from serverFiles import schemas
from bson import ObjectId
from typing import List


prod_api = APIRouter(prefix='/prod', tags=['products'])


@prod_api.get('/products', response_model=List[schemas.prod_res])
async def get_all_products():

    products_list = []

    async for collection in PROD_COL.find():
        products_list.append(collection)
    
    return products_list


@prod_api.get('/products/{id}', response_model=schemas.prod_res)
async def get_products_by_id(id: str):
    # try:
    #     ObjectId(id)

    # except Exception as e:
    #     raise HTTPException(status_code=400, detail=f'Provided id: {id} is a primary key !.')

    res = await PROD_COL.find_one({
        '_id' : id
    })
    
    if not res:
        HTTPException(status_code=404, detail=f'id : {id} is not in db !.')

    return res

@prod_api.post('/products', response_model=schemas.prod_res)
async def create_product(data: schemas.prod_req):
    inp_data = data.model_dump(exclude_unset=True)

    res = await PROD_COL.insert_one(inp_data)

    if not res.acknowledged:
        raise HTTPException(status_code=417, detail=f'cannot add details to the db !.')
    
    res = await PROD_COL.find_one({
        '_id': res.inserted_id
    })

    return res

@prod_api.put('/products', response_model=schemas.prod_res)
async def create_product(data: schemas.prod_req, id: str):
    inp_data = data.model_dump(exclude_unset=True)

    # try:
    #     ObjectId(id)

    # except Exception as e:
    #     raise HTTPException(status_code=400, detail=f'Provided id: {id} is a primary key !.')


    res = await PROD_COL.find_one_and_update(
        {'_id' : id},
        {'$set': inp_data}
    )

    if not res.acknowledged:
        raise HTTPException(status_code=417, detail=f'cannot add details to the db !.')
    
    res = await PROD_COL.find_one({
        '_id': res.upserted_id
    })

    return res

@prod_api.delete('/products/{id}')
async def delete_product(id: str):
    # try:
    #     ObjectId(id)

    # except Exception as e:
    #     raise HTTPException(status_code=400, detail=f'Provided id: {id} is a primary key !.')
    
    res = await PROD_COL.delete_one({'_id' : id})

    if not res.deleted_count == 1:
        raise HTTPException(status_code=404, detail=f'id: {id} is not on db !.')
    
    return {'status': 'success'}

@prod_api.delete('/products')
async def delete_all_product():

    res = await PROD_COL.delete_many({})

    if not res.acknowledged:
        raise HTTPException(status_code=500, detail=f'cannot delete products 1.')
    
    return {'status': 'success'}