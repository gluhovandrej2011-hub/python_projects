a = int(input())
b = int(input())
if b > 2*10**9:
    print("ошибка")
if a > 2*10**9:
    print("ошибка")
if a > b:
    print(">")
if a < b:
    print("<")
if a == b:
    print("=")
