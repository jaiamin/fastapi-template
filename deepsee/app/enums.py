from enum import Enum


# class DeepseeEnum(str, Enum):
#     def __str__(self) -> str:
#         return str.__str__(self)
    

class DatasetType(Enum):
    detection = "detection"
    classification = "classification"
    segmentation = "segmentation"