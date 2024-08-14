import datajoint as dj
from utils_v4 import job
import os

schema = dj.Schema("flyte_demo")
image = "raphaelguzman/flyte-demo-task:v0.1.3"
environment_variables = {
    "DJ_HOST": os.getenv("DJ_HOST"),
    "DJ_USER": os.getenv("DJ_USER"),
    "DJ_PASS": os.getenv("DJ_PASS"),
}


@job(container_image=image, environment=environment_variables)
@schema
class Session(dj.Lookup):
    definition = """
    session_id: int
    """
    contents = []
    # contents = [{"session_id": 0}]


@job(container_image=image, environment=environment_variables)
@schema
class Parameter(dj.Lookup):
    definition = """
    param_id: int
    ---
    param_a: float
    param_b: float
    """
    contents = []
    # contents = [{"param_id": 0, "param_a": 5, "param_b": 8}]


@job(container_image=image, environment=environment_variables)
@schema
class Analysis1(dj.Computed):
    definition = """
    -> Session
    -> Parameter
    ---
    result: float
    """

    def make(self, key):
        param_a, param_b = (Parameter & key).fetch1("param_a", "param_b")
        self.insert1(dict(key, result=param_a + param_b))
        print(f"Computed: {key}")


@job(container_image=image, environment=environment_variables)
@schema
class Analysis2(dj.Computed):
    definition = """
    -> Analysis1
    ---
    result: float
    """

    def make(self, key):
        analysis1_result = (Analysis1 & key).fetch1("result")
        self.insert1(dict(key, result=analysis1_result**2))
        print(f"Computed: {key}")
