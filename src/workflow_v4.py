import datajoint as dj
import pipeline_v4
from utils_v4 import flow
from typing import List


@flow
def flow1(session_rows: List[dict], parameter_rows: List[dict]):
    return dict(
        diagram=dj.Di(pipeline_v4.schema),
        package_name="pipeline_v4",
    )
