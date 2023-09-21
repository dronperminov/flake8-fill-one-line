from typing import Dict, Tuple


def f(a,
      b,
      c):
    return a + b * c


def f1(a: int, b: int,
       c: Dict[str, int]):
    a += b * c["a"]
    c["a"] = a
    return "some"


def f2(a: str,
       b: Tuple[str, Tuple[int, int]], *some_args, **kwargs_name) -> str:
    pass


def f3(arg1: int, arg2: str = 67,
       arg3: str = "abacaba",
       arg4: Tuple[int, int] = (1, 2)) -> Tuple[int, int, str]:
    return arg1 + int(arg2), arg4[0] + arg4[1], arg3


def f4(arg1=5,
       arg2: int = 7,
       arg3="bla"):
    pass


class B:
    def __init__(self,
                 a: int,
                 b: int) -> None:
        pass

    @staticmethod
    def b(a, b, c,
          d,
          e,
          arg1: bool,
          arg2: bool):
        return a + b - c * d / e ^ (arg1 and arg2)
