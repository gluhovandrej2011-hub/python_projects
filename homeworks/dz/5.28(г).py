a = int(input("введите число"))
b = int(input("введите число равное или больше, чем предыдущее"))
result = b - a
arifm = 1

while result<0:
    result = result +(-result)
    print("ошибка, введите так, чтобы первое было меньше второго или равно ему")

while a <= b:
    arifm = arifm * a
    a = a + 1
print(f"произведение всех целых чисел: {arifm}")