import numpy as np


class A:
    def a(self, value: float, arg1: int, arg2: str) -> int:
        return 5

    def b(self, ai: int) -> None:
        print("some text")
        self.a(5.0,
                   arg2="some",
                   arg1=-5)

        self.a(5.0,
               arg2="some",
               arg1=-5).to_bytes()
        print(ai)


class SomeClass:
    def f1(self, img_bin: np.ndarray, task: str) -> np.ndarray:
        # Defining a kernel length

        if task == "orientation":
            length_div = 13
            height_div = 13
        elif task == "finance":
            length_div = 30
            height_div = 20
        elif task == "tables":
            length_div = 55
            height_div = 100

        return img_bin

    def f2(self, img_bin: np.ndarray, task: str):
        # Defining a kernel length

        if task == "orientation":
            length_div = 13
            height_div = 13
        elif task == "finance":
            length_div = 30
            height_div = 20
        elif task == "tables":
            length_div = 55
            height_div = 100

        return img_bin
