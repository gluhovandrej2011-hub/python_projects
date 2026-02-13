import random

comp_number = random.randint(1, 100)
user_number = 0

count_tries = 0

left_side = 1
rigth_side = 100

print(f"Я загадал число от {left_side} до {rigth_side}. Попробуй отгадай!")

while user_number != comp_number:

    count_tries = count_tries + 1

    user_number = int(
        input(
            f"Попытка №{count_tries}. Введите своё число от {left_side} до {rigth_side}: "
        )
    )

    if user_number == 777:
        print(f"правильный ответ = {comp_number}")

    if user_number > comp_number:
        print("Введите поменьше")
        rigth_side = user_number - 1
    elif user_number < comp_number:
        print("Введите побольше")
        left_side = user_number + 1
    else:
        print("Вы угадали")

if count_tries <= 5:
    print("Вы гений!")
elif count_tries > 5 and count_tries <= 10:
    print("Неплохо!")
elif count_tries > 10 and count_tries <= 15:
    print("Вы дно!")
else:
    print("Закрой игру и не открывай больше))))")