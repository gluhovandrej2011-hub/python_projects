x = int(input())
y = int(input())
z = int(input())
if x > 1000:
    print("impossible")
if y > 1000:
    print("impossible")
if z > 1000:
    print("impossible")
if x + y < z:
    print("impossible")
else:
    v = x + y - z
    print(f"{v}")