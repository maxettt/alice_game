import requests
import json
from operator import itemgetter



def open_json():
    with open("alice_game.json", "r", encoding="utf-8") as f:
        table = json.load(f)
    return table


def write_json(table):
    with open("alice_game.json", "w", encoding="utf-8") as f:
        json.dump(table, f, indent=1, ensure_ascii=False)


def check_pass(name, table):
    """Функция принимает имя пользователя и проверяет не играл ли пользователь с таким именем.
     И если уже играл до этого просит авторизоватся с помощью пароля.
        Возвращает True если пользователь участвовал в игре, и false если поьзователь играет в первый раз
        А также в случае неправильного ввода пароля 3 раза прекращает игру"""
    names = [] #создаем пустой список в который будем записывать имена из переменной table
    for i in range(len(table)): #пробегаемся по значениям  переменной table
        names.append(table[i]["name"]) #Заполняем список names именами из table

    if name in names: #Если введенное пользователем имя есть в списке имен
        index = names.index(name) # переменной index присваиваем порядковый номер этого имени
        for i in range(3): #запускаем цикл 3 раза
            password = input("Введите пароль\n") # Просим пользователя ввести пароль
            if password != table[index]["pass"]: # Если пароль неверный (не соответствует значению в переменной table)
                print(f"Неправильный пароль. Осталось попыток - {3-i-1}") # предупреждаем пользователя - пароль неверный
                                                                    # и пишем оставшееся количество попыток ввода пароля
                if i == 2:
                    print("Вы не смогли авторизоваться")
                    exit()  #После 3 неудачных попыток авторизации попыток программа закрывается
            else:
                return True

    else:
        return False


def hello():
    """Программа приветствует пользователя с именем, полученным
    из пользовательского ввода. Добавляет его запись в файл.
    И возвращает файл с новой записью пользователя"""
    table = open_json() #В переменную table передаем содержимое файла alice_game.json

    print("Привет, давай поиграем в игру, где нужно составлять несколько слов из одного слова")
    name = input("Введите имя игрока\n") #В переменную name передаем имя игрока, которое введено с клавиатуры
    if not check_pass(name, table): # Если пользователь играет в первый раз.
        print(f"{name}, добро пожаловать в игру")
        password = input("Введите пароль к своей учетной записи\n") # программа просит ввести пароль,
                                                                    # т.е. зарегистрироваться в игре
        print("Так как Вы играете впервые предлагаю посмотреть статистику других игроков")
        form_table(table)   # для новых игроков будет сформирована таблица с именами игроков и словами с которыми
                            # уже играли другие игроки
        words = {}
        user = {}
        for word in table[0]["words"]:
            words[word] = []
        user["name"], user["pass"], user["words"] = name, password, words
        table.append(user)
        table = sort_user(table)
        write_json(table)
    else:
        answer = input("Если хотите посмотреть статистику других игроков, нажмите (Y)\n")
        if answer.lower() == "y":
            form_table(table)
    return name


def add_word_in_table(word, table):
    if not is_word_in_table(word, table):
        for i in range(len(table)):
            table[i]["words"][word] = []
        table = sort_table(table)
        write_json(table)
    return table


def input_word():
    """Программа запрашивает у пользователя реально существующее слово (существительное) :), с которым он будет играть"""
    word = input("Введите слово (существительное), с которым будем играть\n")
    while selection_of_words(word) == []:
        print(f"Слова {word} для игры не подходит, выберите другое слово\n")
        word = input("Введите слово (существительное), с которым будем играть\n")
    return word


def is_word_in_table(word, table):
    if word in table[0]["words"]:
        return True
    return False


def selection_of_words(word):
    """Возвращает список существующих слов, составленных из слова, передаваемого функции.
     Список формируется по requests запросу с сайта https://slogislova.ru/iz_bukv"""
    #print(f"Существующие слова из слова '{word}':")
    response = requests.get(f"https://slogislova.ru/iz_bukv/{word}")
    start = response.text.find("Cлова cоставленные из не повторяющихся букв")
    stop = response.text.find("Слова из повторяющихся букв")
    text = response.text[start:(stop+27)]
    # print(text)
    words = []
    while "<span>" in text:
        start = text.find("<span>")
        stop = text.find("</span>")
        words.append(text[(start + 6):(stop)])
        text = text.replace("<span>", "", 1)
        text = text.replace("</span>", "", 1)

    if word in words:
        words.remove(word)  #Если исходное слово, переданное функции (введенное пользователем) существует,
        return words        #то оно окажется в списке слов. Возвращаем список "подслов" без исходного слова
    else:
        return []                     #Если исходное слово, переданное функции (введенное пользователем) не существует,
                                      #то возвращаем пустой список.


def set_of_words(table):

    words = []
    for word in table[0]["words"]:
        words.append(word)

    words.sort()
    return words


def set_of_names(table):

    names = []
    for i in range(len(table)):
        names.append(table[i]["name"])

    return names


def max_length_words(words):

    max_length_word = 0

    for word in words:
        if len(word) > max_length_word:
            max_length_word = len(word)

    return max_length_word


def max_length_names(names):

    max_length_name = 0

    for name in names:
        if len(name) > max_length_name:
            max_length_name = len(name)

    return max_length_name


def form_table(table):
    print()
    names = set_of_names(table) #формируем список имен игроков
    words = set_of_words(table) #формируем список слов с которыми уже играли пользователи
    max_length_name = int(max_length_names(names)) #В переменную max_length_name записываем длину
                                                   # максимально длинного имени пользователя
    max_length_word = int(max_length_words(words))
    print("".ljust(max_length_name + 3), "", end="")
    for key in table[0]["words"].keys():
        print(key+" ("+str(len(selection_of_words(key)))+")", "   ", end="")
    print()
    for i in range(len(table)):
        print(table[i]["name"].ljust(max_length_name + 3), "", end="")
        for key, value in table[i]["words"].items():
            print(len(value), " ".ljust(len(key)+5)+" ".ljust(len(str(len(selection_of_words(key))))), end="") #
        print()
    print()

def sort_table(table):
    for i in range(len(table)):
        t = sorted(table[i]["words"].items())
        #print(t)
        table[i]["words"] = dict(t)

    return table


def sort_user(table):
    table = sorted(table, key=itemgetter("name"))
    return table


def check_word(name, word, table):
    count_word = 0
    count_right_answer = 0
    gamer = "none"
    sub_words = selection_of_words(word)
    asked_sub_words = []
    for i in range(len(table)):
        if len(table[i]["words"][word]) > count_word:
            count_word = len(table[i]["words"][word])
            gamer = table[i]["name"]
    print("Отлично, теперь можем начать игру.")
    print("Чтобы закончить игру введите 'quit'.")
    print(f"Из слова '{word}' можно составить '{len(selection_of_words(word))}' подслов.")
    print(f"Текущий рекорд принадлежит игроку '{gamer}' - {count_word} угаданных слов.")
    wrd = ""
    while wrd != "quit" and count_right_answer != len(selection_of_words(word)):

        wrd = input("Ваше слово... \n")
        if wrd in asked_sub_words:
            print("Это слово уже было")
        elif wrd in sub_words:
            count_right_answer += 1
            print(f"Принято. Угадано слов - {count_right_answer}")
            asked_sub_words.append(wrd)
        else:
            print("Неверно, попробуйте другое слово")



    if count_right_answer == len(selection_of_words(word)):
        print(f"Вы угадали максимальное количество слов - {count_right_answer}")
        for i in range(len(table)):
            if name == table[i]["name"]:
                table[i]["words"][word] = asked_sub_words

    if wrd == "quit":
        print(f"Спасибо за игру. Было весело. Вы угадали {count_right_answer} слов")
        for i in range(len(table)):
            if name == table[i]["name"]:
                table[i]["words"][word] = asked_sub_words

    write_json(table)




# name = hello()
# word = input_word()
# words = selection_of_words(word)
# table = open_json()
# add_word_in_table(word, table)
# table = open_json()
# check_word(name, word, table)













