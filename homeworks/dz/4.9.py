ms = int(input("м/с"))
kmh = int(input("км/ч"))
r = kmh - ms * 3.6
if r > 0:
    print("cкорость в км/ч больше")
elif r < 0:
    print("скорость в м/с больше")
else:
    print("скорости равны")
