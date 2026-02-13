x = int(input("введите число"))
v = x
ch = x
first = 0
nums = 0
while v >= 10:
    v = v // 10
first = v
while ch > 0:
    tc = ch % 10
    if tc == first:
        nums = nums + 1
    ch = ch // 10
print(f"в числе {x} первая цифра встречается {nums} раз")