# Truss External Packages for Fun and Profit

The goal of this repo is to provide an example of how to use the external packages feature of [truss](https://github.com/basetenlabs/truss). This README will be more of a tutorial style to allow you to recreate a truss which uses external code.

The goal of the external packages feature is to allow code maintained outside of the truss itself to be used inside the truss (and potentially multiple trusses). The main goal here is code reuse and allowing for all the healthy gitops and testing that python teams are used and separating those concerns from truss.

## Fun

### Setup external packages
To demonstrate,  I've created two simple packges inside `shared/` to represent the code that is maintained outside of the truss that I want to reuse. It's a very simple dataclass and a helper/utility method for demonstration.

### Create Truss and reference packages
Let's go ahead and create the truss
```bash
truss init reuse_truss
```

Let's take a look inside the [`config.yaml`](./reuse_truss/config.yaml#L6) in the newly created truss and we'll notice that there is a new entry:
```yaml
external_package_dirs: []
```

This key holds a list of all the directories that I want to be accessible inside the code that I write in my truss. Since we want to access both packages in our `shared/` directory, let's update this key to:
```yaml
external_package_dirs:
- ../shared/
```

> Note on paths: The path of the external packages must be relative to the `config.yaml` file. So `shared/` is the parallel to `reuse_truss`, but it's one directory up from the config so we use `../shared`.

With this change, any of the code inside `shared/` will be accessible for us to use inside our `model.py`. To demonstrate this, let's consider that what I want this truss to do is to contruct two [`InventoryItem`'s](./shared/pkg1/types.py#L4) and [swap their prices](./shared/pkg2/methods.py#L3).

### Using external packages
For me, it's easier to iterate with truss using an IPython style kernel/notebook. So I'm gonna jump into a kernel.

Let's start by constructing the example input we want and adding it to the truss for easy testing later.

```python
In [1]: import truss

In [2]: my_truss = truss.load("./reuse_truss")

In [3]: example_input = {"obj1": {"name": "apples", "unit_price": 10.0, "quantity_on_hand": 5}, "obj2": {"name": "oranges", "unit_price": 5.0, "quantity_on_hand":19}}

In [4]: my_truss.add_example("test1", example_input)
```

Keep that shell running, and let's hop into `model.py` and update the file to do what we want. I've pasted the result below
```python
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
```

Now let's jump back in the shell to test what we wrote.
```python
In [5]: my_truss.predict(example_input)
Out[5]: 
{'obj1': {'name': 'apples', 'unit_price': 5.0, 'quantity_on_hand': 5},
 'obj2': {'name': 'oranges', 'unit_price': 10.0, 'quantity_on_hand': 19}}
```

Great! We know this works locally and it can access my shared library. Now what about if I deploy to any web service? The way we can make sure of that is by running in Docker. Truss makes it easy
```python
In [6]: my_truss.docker_predict(example_input)
Out[6]: 
 => [internal] load build definition from Dockerfile                                                                                                      0.3s
 => => transferring dockerfile: 374B                                                                                                                      0.0s
 => [internal] load .dockerignore                                                                                                                         0.4s
 => => transferring context: 2B                                                                                                                           0.0s
 => [internal] load metadata for docker.io/baseten/truss-server-base:3.9-v0.2.4                                                                           0.2s
...
 => exporting to image                                                                                                                                    4.2s
 => => exporting layers                                                                                                                                   3.8s
 => => writing image sha256:ccb33c661b8286c364d00dd94029ffbbda9974bdf842266b587d58f7b68f81c1                                                              0.0s
 => => naming to docker.io/library/custom-model:latest                                                                                                    0.0s
Model server started on port 8080, docker container id 987fb92209990b84d848bbf77d4eb4788f41c7526907335a1603ed2af7e198ea
INFO:truss.truss_handle:Model server started on port 8080, docker container id 987fb92209990b84d848bbf77d4eb4788f41c7526907335a1603ed2af7e198ea
Container state: DockerStates.RUNNING
INFO:truss.truss_handle:Container state: DockerStates.RUNNING
{'obj1': {'name': 'apples', 'unit_price': 5.0, 'quantity_on_hand': 5},
 'obj2': {'name': 'oranges', 'unit_price': 10.0, 'quantity_on_hand': 19}}
```

### Profit!
Nice! So we're even good to deploy it remotely. From here, we can simply modify the code inside the truss or inside the shared package and we should be good to go. Maybe try swapping the name instead and see the results for yourself.

Happy Truss'in!