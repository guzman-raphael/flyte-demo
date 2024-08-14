import functools
from typing import List, Optional
from flytekit import task, workflow
import inspect
import importlib
from datajoint.diagram import _get_tier
from datajoint.user_tables import Lookup, Manual, Computed, Imported
from datajoint.user_tables import TableMeta


def job(container_image, environment):
    def inner_decorator(cls):
        def wrapped(
            rows: Optional[List[dict]] = None, parents: Optional[List[str]] = None
        ) -> str:
            if issubclass(_get_tier(cls.full_table_name), (Lookup, Manual)):
                import time

                print(f"inserting session: {rows}")
                cls.insert(rows)
                time.sleep(3)
                return cls.__name__
            elif issubclass(_get_tier(cls.full_table_name), (Imported, Computed)):
                import time

                print(f"computing records: {cls.__name__}")
                cls.populate()
                time.sleep(3)
                return cls.__name__

        wrapper_sig = inspect.signature(wrapped)
        wrapper_annotations = wrapped.__annotations__

        functools.update_wrapper(wrapped, cls)

        wrapped.__signature__ = inspect.signature(wrapped).replace(
            parameters=[
                p.replace(kind=inspect.Parameter.KEYWORD_ONLY)
                for p in wrapper_sig.parameters.values()
            ],
            return_annotation=wrapper_sig.return_annotation,
        )
        wrapped.__annotations__ = wrapper_annotations

        cls.task = task(
            wrapped, container_image=container_image, environment=environment
        )
        cls.name = cls.task.name
        cls.dispatch_execute = cls.task.dispatch_execute
        return cls

    return inner_decorator


def flow(func):
    @workflow
    @functools.wraps(func)
    def wrapped(session_rows: List[dict], parameter_rows: List[dict]):
        data = func(session_rows=session_rows, parameter_rows=parameter_rows)
        diagram = data["diagram"]
        package = importlib.import_module(
            data["package_name"], package=data["package_name"]
        )

        graph = dict()
        for class_name, table in package.__dict__.items():
            if (
                isinstance(table, TableMeta)
                and table.full_table_name in diagram.nodes_to_show
            ):
                if issubclass(_get_tier(table.full_table_name), (Lookup, Manual)):
                    graph[table.full_table_name] = package.__dict__[class_name].task(
                        rows=vars()[f"{class_name.lower()}_rows"],
                        parents=[graph[t] for t in graph if t in table.parents()],
                    )
                elif issubclass(_get_tier(table.full_table_name), (Imported, Computed)):
                    graph[table.full_table_name] = package.__dict__[class_name].task(
                        parents=[graph[t] for t in graph if t in table.parents()]
                    )

    return wrapped
