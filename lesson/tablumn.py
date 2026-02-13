a = 1
b = 0

while a <= 9:
    while b <= 9:
        b = b + 1
        c = a * b
        print(f"{a}*{b}={c}")
    b = 1
    a = a + 1
