# -*- coding: utf-8 -*-

import gorilla

import tests.utils.tomodule


@gorilla.patch(tests.utils.tomodule, name='function0')
def function():
    """subpackage.function"""
    return "subpackage.function"
