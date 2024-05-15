from typing import Dict, List, Optional, Tuple


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

    def _parse_document(self, path: str, parameters: dict, another_field: Optional[str], some_arg_two: Optional[str]) -> Tuple[List[int],
                                                                                                                               List[dict],
                                                                                                                               List[float],
                                                                                                                               List[str],
                                                                                                                               Optional[dict]]:
        first_page = 0 if parameters["first_page"] is None or parameters["first_page"] < 0 else parameters["first_page"]
        return [], [], [], [], None

    def _parse_document2(self, path: str, parameters: dict) -> Tuple[List[int], List[dict],
                                                                    List[float], List[str],
                                                                    Optional[dict]]:
        first_page = 0 if parameters["first_page"] is None or parameters["first_page"] < 0 else parameters["first_page"]
        return [], [], [], [], None


class C:
    def __init__(self, *, config: Optional[dict] = None) -> None:
        self.config = config


class D:
    def __init__(self, *, config: Optional[dict] = None,
                 a: str,
                 b: int = 123_456_789,
                 c="dewfhrihieh") -> None:
        self.config = config
        self.a = b
        self.b = a

    def not_init(self, *, config: Optional[dict] = None,
                 a: str,
                 b: int = 123_456_789,
                 c="dewfhrihieh",
                 d: str = "dewoifhgroithiowjeirothiwrh") -> None:
        pass

    def another1(self, *, config: Optional[dict] = None,
                 a: str,
                 b: int = 123_456_789,
                 c="dewfhrihieh",
                 d: str = "dewoifhgroithiowjeirothiwrh12345678") -> None:
        pass

    def another2(self, *, config: Optional[dict] = None,
                 a: str,
                 b: int = 123_456_789,
                 c="dewfhrihieh",
                 d: str = "dewoifhgroithiowjeirothiwrh123456789") -> None:
        pass
