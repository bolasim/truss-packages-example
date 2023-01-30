from typing import Dict, List
from pkg1.types import InventoryItem
from pkg2.methods import swap_prices
from dataclasses import asdict

class Model:
    def __init__(self, **kwargs) -> None:
        self._data_dir = kwargs["data_dir"]
        self._config = kwargs["config"]
        self._secrets = kwargs["secrets"]
        self._model = None

    def load(self):
        # Load model here and assign to self._model.
        pass

    def preprocess(self, request: Dict) -> Dict:
        """
        Incorporate pre-processing required by the model if desired here.

        These might be feature transformations that are tightly coupled to the model.
        """
        return request

    def postprocess(self, request: Dict) -> Dict:
        """
        Incorporate post-processing required by the model if desired here.
        """
        return request

    def predict(self, request: Dict) -> Dict[str, List]:
        response = {}
        obj1 = InventoryItem(**request["obj1"])
        obj2 = InventoryItem(**request["obj2"])
        swap_prices(obj1, obj2)
        return {
            "obj1": asdict(obj1),
            "obj2": asdict(obj2),
        }
