from typing import Annotated
from collections import defaultdict

from pydantic import BaseModel, Field

from fastapi import FastAPI, Body

from starlette.exceptions import HTTPException

app = FastAPI()

ds = defaultdict(lambda: defaultdict(dict))


class Image(BaseModel):
    imageId: Annotated[str, Field(ge=1)]
    imageData: str


def dataset_exists(id):
    return id in ds


def image_exists(id, imageId):
    assert id in ds
    return imageId in ds[id]


@app.get('/')
def root():
    return {'note': 'nothing to see here'}


@app.post('/datasets')
def create_dataset(
    id: Annotated[str, Body(embed=True, ge=1)]
):
    if dataset_exists(id):
        return {'error': f'Dataset {id} already exists'}
    ds[id] = defaultdict(dict)
    return {'success': f'Dataset {id} created'}


@app.delete('/datasets')
def delete_dataset(id: Annotated[str, Body(embed=True)]):
    if not dataset_exists(id):
        return {'error': f'Dataset {id} does not exist'}
    del ds[id]
    return {'success': f'Dataset {id} deleted'}


@app.post('/datasets/{id}/images')
def add_image_to_dataset(
    id: str, 
    img: Image, 
):
    if not dataset_exists(id):
        return {'error': f'Dataset {id} does not exist'}
    if image_exists(id, img.imageId):
        return {'error': f'Image ID {img.imageId} already exists'}
    ds[id][img.imageId] = img.imageData
    return {'success': f'Image {img.imageId} added'}


@app.delete('/datasets/{id}/images')
def delete_image_from_dataset(id: str, imageId: Annotated[str, Body()]):
    if not dataset_exists(id):
        return {'error': f'Dataset {id} does not exist'}
    if not image_exists(id, imageId):
        return {'error': f'Image {imageId} does not exist'}
    del ds[id][imageId]
    return {'success': f'Image {imageId} deleted'}


@app.get('/datasets')
def list_datasets():
    return {'datasets': list(ds.keys())}


@app.get('/datasets/{id}/images')
def list_images(id: str):
    if not dataset_exists(id):
        return {'error': f'Dataset {id} does not exist'}
    return {'images': list(ds[id].keys())}


@app.get('/datasets/{id}/images/stats')
def get_dataset_stats(id):
    if not dataset_exists(id):
        return {'error': f'Dataset {id} does not exist'}
    data = ds[id]
    return {'num_images': len(data)}