from fastapi import APIRouter, HTTPException, status
from serverFiles.database import CARTS
from serverFiles import schemas
from bson import ObjectId
from typing import List


cart_api = APIRouter(prefix='/prod', tags=['carts'])


@cart_api.get('/carts', response_model=List[schemas.carts_res])
async def get_all_carts():


    carts_list = []

    async for collection in CARTS.find():
        carts_list.append(collection)
    
    return carts_list


@cart_api.get('/carts/{id}', response_model=schemas.carts_res)
async def get_carts_by_id(id: str):
    try:
        ObjectId(id)

    except Exception as e:
        raise HTTPException(status_code=400, detail=f'Provided id: {id} is a primary key !.')

    res = await CARTS.find_one({
        '_id' : ObjectId(id)
    })
    
    if not res:
        HTTPException(status_code=404, detail=f'id : {id} is not in db !.')

    return res

@cart_api.post('/carts', response_model=schemas.carts_res)
async def create_carts(data: schemas.carts_req):
    inp_data = data.model_dump(exclude_unset=True)

    res = await CARTS.insert_one(inp_data)

    if not res.acknowledged:
        raise HTTPException(status_code=417, detail=f'cannot add details to the db !.')
    
    res = await CARTS.find_one({
        '_id': res.inserted_id
    })

    return res

@cart_api.put('/carts', response_model=schemas.carts_res)
async def create_carts(data: schemas.carts_req, id: str):
    inp_data = data.model_dump(exclude_unset=True)

    try:
        ObjectId(id)

    except Exception as e:
        raise HTTPException(status_code=400, detail=f'Provided id: {id} is a primary key !.')


    res = await CARTS.find_one_and_update(
        {'_id':ObjectId(id)},
        {'$set': inp_data}
    )

    if not res.acknowledged:
        raise HTTPException(status_code=417, detail=f'cannot add details to the db !.')
    
    res = await CARTS.find_one({
        '_id': res.upserted_id
    })

    return res

@cart_api.delete('/carts/{id}')
async def delete_carts(id: str):
    try:
        ObjectId(id)

    except Exception as e:
        raise HTTPException(status_code=400, detail=f'Provided id: {id} is a primary key !.')
    
    res = await CARTS.delete_one({'_id':ObjectId(id)})

    if not res.deleted_count == 1:
        raise HTTPException(status_code=404, detail=f'id: {id} is not on db !.')
    
    return {'status': 'success'}

@cart_api.delete('/carts')
async def delete_all_carts():

    res = await CARTS.delete_many({})

    if not res.acknowledged:
        raise HTTPException(status_code=500, detail=f'cannot delete carts 1.')
    
    return {'status': 'success'}