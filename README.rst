====================
flake8-fill-one-line
====================

A Flake8 plugin to ensure an expression can be written in one line without exceeding the maximum length (``160`` characters by default) limit.

Installation
------------

Install from ``pip`` with:

.. code-block:: bash

    pip install flake8-fill-one-line

Reported errors
---------------

====== ====
 Code  Rule
====== ====
FOL001 ``import`` statement can be written in one line
FOL002 function call can be written in one line
FOL003 assignment can be written in one line
FOL004 ``return`` statement can be written in one line
FOL005 function definition can be written in one line
FOL006 ``with`` statement can be written in one line
FOL007 ``if`` statement can be written in one line
====== ====

Used options
------------

* ``max_line_length`` - option from Flake8, length limit for line
* ``skip-std-names`` - ignore ``tuple()``, ``list()``, ``set()``, ``dict()`` calls (used by default)
* ``skip-multiline-arguments`` - ignore function calls with arguments on multiple lines (used by default)


Examples
--------

* Imports:

.. code-block:: python

    # wrong:
    import sys, \
        argparse
    from random import randint as rand_int, \
        sample, choice as \
        random_choice

    # right:
    import sys, argparse
    from random import randint as rand_int, sample, choice as random_choice

* Calls and assignments

.. code-block:: python

    # wrong:
    f(1, 2, 3,
      4, 5, 6, 7,
      8, 9)

    # right:
    f(1, 2, 3, 4, 5, 6, 7, 8, 9)


    # wrong:
    some_var = foo(1,
                   a=3,
                   b=42)

    # right:
    some_var = foo(1, a=3, b=42)


    # wrong:
    def f(a: int, b: int) -> int:
        return f1(a,
                  b,
                  a + b)

    # right:
    def f(a: int, b: int) -> int:
        return f1(a, b, a + b)


    # wrong:
    def foo(a: int, b: int):
        return a - b * 3 if \
            b < 4 \
            else foo(a - 1, b + 1)

    # right:
    def foo(a: int, b: int):
        return a - b * 3 if b < 4 else foo(a - 1, b + 1)

* Function definitions

.. code-block:: python

    # wrong
    def f(a,
          b,
          c):
        return a + b * c

    # right:
    def f(a, b, c):
        return a + b * c


    # wrong
    def f2(
            a: str,
            b: tuple, *some_args,
            **kwargs_name
           ) -> str:
        pass

    # right:
    def f2(a: str, b: tuple, *some_args, **kwargs_name) -> str:
        pass

* With statements

.. code-block:: python

    # wrong:
    with open("some_file.txt") as \
            f:
        f.read()

    # right:
    with open("some_file.txt") as f:
        f.read()


    # wrong:
    with open("f1.txt") as f1, \
            open("f2.txt", "w") as f2:
        f2.write(f1.read())

    # right:
    with open("f1.txt") as f1, open("f2.txt", "w") as f2:
        f2.write(f1.read())

* If statements

.. code-block:: python

    # wrong:
    if (
        a < b and
        c < d and
        a + b == c - d
    ):
        pass

    # right:
    if a < b and c < d and a + b == c - d:
        pass


    # wrong:
    if a < \
            b:
        pass

    # right:
    if a < b:
        pass


    # wrong:
    for i in range(100):
        if (i < 5 or
                i > 10):
            pass
        elif i == 2 or \
            i == 3 or i == 11 \
                or i == 28:
            pass
        elif 47 <= i <= 58:
            pass
        elif i * (20 -
                  i) < 0:
            pass

    # right:
    for i in range(100):
        if i < 5 or i > 10:
            pass
        elif i == 2 or i == 3 or i == 11 or i == 28:
            pass
        elif 47 <= i <= 58:
            pass
        elif i * (20 - i) < 0:
            pass
