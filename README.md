# flake8-fill-one-line
A Flake8 plugin to ensure an expression can be written in one line without exceeding the maximum length (`160` characters by default)

## Reported errors

* `FOL001`: a function call can be written in one line
* `FOL002`: an assignment can be written in one line
* `FOL003`: a function definition can be written in one line
* `FOL004`: an import can be written in one line

## Examples

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


# wrong:
f(1, 2, 3,
  4, 5, 6, 7,
  8, 9)
some_var = foo(1,
             a=3,
             b=42)

# right:
f(1, 2, 3, 4, 5, 6, 7, 8, 9)
some_var = foo(1, a=3, b=42)
```
