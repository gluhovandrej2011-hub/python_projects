question = ""
guess_word = ""
user_word = ""

question = input("введите вопрос-подсказку для загаданного слова: ")
guess_word = input("введите правильное слово: ")

user_word = "*" * len(guess_word)

print("\n" * 50)

game_is_run = True
while game_is_run == True:
    print(f"ВОПРОС: {question}")
    print(f"ОТГАДАННОЕ СЛОВО: {user_word}")

    letter = input("введите предполагаемую букву в слове: ")

    if guess_word.find(letter) == -1:
        print("такой буквы нет")
    else:
        temp =""
        for i in range(len(guess_word)):
            if guess_word[i] == letter:
                temp += guess_word[i]
            else:
                temp += user_word[i]
        user_word = temp

        if user_word.find("*") == -1:
            game_is_run = False