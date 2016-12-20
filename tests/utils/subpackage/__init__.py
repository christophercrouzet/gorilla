import gorilla

from tests.utils import tomodule


@gorilla.patch(tomodule, name='function0')
def function():
    """subpackage.function"""
    return "subpackage.function"
