import math

a = 5
b = math.e
c = -4

if a < b:
    c = a

if a < c:
    d = b
else:
    d = a

if d + a < b - c:
    result = "1"
elif d + a > b + c:
    result = "2"
else:
    result = "0"

if (
        a < b and
        c < d and
        a + b == c - d
):
    result = "unknown"

if a < \
        b:
    pass

items = []
for i in range(100):
    if (i < 5 or
            i > 10):
        items.append(i)
    elif i == 2 or \
        i == 3 or i == 11 \
            or i == 28:
        items.append(i * i)
    elif 47 <= i <= 58:
        items.append(-i*2)
    elif i * (20 -
              i) < 0:
        items.append(0)
