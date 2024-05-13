from sqlalchemy.orm import Session

from app import models


def get_stats(*, session: Session):
    dataset_count = session.query(models.Dataset).count()
    user_count = session.query(models.User).count()
    image_count = session.query(models.Image).count()
    return {
        'dataset_count': dataset_count,
        'user_count': user_count,
        'image_count': image_count,
    }