from typing import Any, Dict

from sqlalchemy.orm import as_declarative

class_registry: Dict[str, Any] = {}


@as_declarative(class_registry=class_registry)
class Base:
    id: Any
    __name__: str
    __abstract__: bool = True