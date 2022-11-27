import inspect

from . import test_module


def inject_dependencies(function, dependencies):
    params = inspect.signature(function).parameters

    deps = {
        name: dependency for name, dependency in dependencies.items() if name in params
    }
    return lambda message: function(message, **deps)


def bootstrap():

    dependencies = {"dependency_1": "test", "dependency_2": "test"}

    functions = inspect.getmembers(test_module, inspect.isfunction)
    injected_functions = {}

    for function in functions:
        function_name, function = function
        setattr(test_module, function_name, inject_dependencies(function, dependencies))
