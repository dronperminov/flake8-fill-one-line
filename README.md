# flake8-fill-one-line
A Flake8 plugin to ensure an expression can be written in one line without exceeding the maximum length (`160` characters by default)

## Reported errors

* `FOL001`: `import` statement can be written in one line"
* `FOL002`: function call can be written in one line
* `FOL003`: assignment can be written in one line
* `FOL004`: `return` statement can be written in one line
* `FOL005`: function definition can be written in one line

## Examples

* Imports:
```python
# wrong: 
import sys, \
    argparse
from random import randint as rand_int, \
    sample, choice as \
    random_choice

# right: 
import sys, argparse
from random import randint as rand_int, sample, choice as random_choice
```

* Calls and assignments
```python
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
```

* Function definitions
```python
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
```
