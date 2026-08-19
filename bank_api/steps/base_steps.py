from typing import List, Any


class BaseSteps:
    def __init__(self, created_obj: List[Any]):
        self.session = None
        self.created_obj = created_obj

