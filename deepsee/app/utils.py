from enum import Enum


class DatasetType(Enum):
    Detection = "Object Detection"
    Classification = "Classification"
    Segmentation = "Segmentation"