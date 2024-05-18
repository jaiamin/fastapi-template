from fastapi import APIRouter, HTTPException, status

from app import crud
from app.enums import DatasetType
from app.api.deps import SessionDep, CurrentUser
from app.schemas import (
    DatasetCreate,
    DatasetPublic, 
    ImagePublic,
)

router = APIRouter()

@router.get('/', response_model=list[DatasetPublic])
def get_datasets(*, session: SessionDep):
    """Retrieves all datasets stored on deepsee (with pagination)."""
    return crud.get_datasets(session=session)


@router.get('/my', response_model=list[DatasetPublic])
def get_current_user_datasets(*, session: SessionDep, current_user: CurrentUser):
    """Retrieves the datasets belonging to the current session user."""
    return crud.get_user_datasets(session=session, uid=current_user.id)


@router.post('/', response_model=DatasetPublic)
def create_dataset(*, session: SessionDep, current_user: CurrentUser, dataset_in: DatasetCreate):
    """Creates a new deepsee dataset for a given user."""
    dataset = crud.get_dataset_by_title(session=session, dataset_title=dataset_in.title)
    if dataset:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='This dataset title is taken.'
        )
    new_dataset = crud.create_dataset(session=session, dataset_in=dataset_in, uid=current_user.id)
    return new_dataset


@router.put('/')
def update_dataset():
    """
    Updates the metadata of a given deepsee dataset.
    Note: This does not handle adding/removing images from a dataset.
    """
    pass


@router.delete('/')
def delete_dataset():
    """Deletes a given dataset belonging to the current session user."""
    pass 


@router.get('/{dataset_id}')
def get_dataset(*, session: SessionDep):
    """Retrieves a specific dataset stored on deepsee by ID."""
    pass