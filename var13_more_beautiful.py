""" Вариант 13. Имеется толковый словарь. Каждому слову может соответствовать несколько значений, 
для каждого значения должен быть как минимум один пример употребления. 
Разработать структуру данных для хранения словаря, его записи/чтения на диск. 
Слова хранить упорядоченными по алфавиту.
"""


# В общем виде структура данных такова: префиксное дерево, в узлах которого
# хранятся буквы, причём каждая буква - ключ словаря, значение которого - 
# словарь с возможными вариантами следующей буквы.
#
# В значении последней буквы слова тоже словарь, ключ которого - символ *,
# значение - массив, каждый элемент которого - словарь с толкованием
# слова в ключе и массивом примеров в значении.

# Пример для толкового словаря из .json со словами А, АБ, АБАЖУР, АБЗАЦ, БАЛ, БАЛЛ
# (хранятся в алфавитном порядке, т.е. в каждом словаре буквы последовательны)

import json
from collections import OrderedDict

# ЧАСТЬ 1. ЧТЕНИЕ

def dictionary_reading(current_node, prefix=''):
    """Выводит словарь в читабельном виде"""

    # Чтобы наверняка сохранилась упорядоченность по алфавиту
    current_node = OrderedDict(current_node.items())
    # Перебираем буквы-ключи и их поддеревья
    for letter, value in current_node.items():
        # Если конец слова, выводим его
        if letter == '*':
            print(prefix, end='. ')
            # Счётчик для определений, чтобы их нумеровать
            number = 1
            # Перебираем словари из определений и примеров как элементы массива
            for definitions in value:
                # Перебираем сами определения и примеры
                for definition, examples in definitions.items():
                    # Если значений больше одного, то нумеруем их и выводим
                    if len(value) > 1:
                        print(str(number) + ". " + definition + " Пример(ы): ", end=" ")
                    # Если одно, то просто выводим
                    else:
                        print(definition + " Пример(ы): ", end=" ")
                    # Выводим пример(-ы)
                    for example in examples:
                        print(example, end=" ")
                # Переходим к следующему определению, увеличиваем счётчик        
                number += 1
            print("\n")
                
        else:
            # Если не конец слова, добавляем к префиксу следующую букву и 
            # рекурсивно вызываем функцию для следующей вершины
            dictionary_reading(value, prefix+letter)


# ЧАСТЬ 2. ЗАПИСЬ

def dictionary_to_list(current_node, listed_result, prefix=''):
    """Записывает словарь в массив, каждый элемент
    которого - строка со словом, определением
    и примерами
    """
    
    # В целом, функция практически как dictionary_reading, 
    # отличия далее комментируются
    current_node = OrderedDict(current_node.items())
    for letter, value in current_node.items():
        if letter == '*':
            # Создаём список для каждой строки словаря
            line = []
            line.append(prefix + ". ")
            number = 1

            for definitions in value:
                for definition, examples in definitions.items():
                    if len(value) > 1:
                        line.append(" " + str(number) + ". " + definition + " Пример(ы): ")
                    else:
                        line.append(definition + " Пример(ы): ")
                    for example in examples:
                        line.append(" " + example)
                number += 1
            # Собираем элемнты списка для строки в строку и добавляем в массив словаря
            listed_result.append(''.join(line))
                
        else:
            dictionary_to_list(value, listed_result, prefix+letter)
    # Возвращаем массив словаря (список строк со словами, значениями и примерами)
    return listed_result

def listed_dictionaty_to_txt(some_list):
    """Загружает данные в .txt"""
    with open("dict_file.txt", "a", encoding="utf-8") as txt:
        for zn in some_list:
            txt.write(str(zn) + '\n')


def main(some_json):
    """Пример работы со словарём в файле .json"""

    with open(some_json, encoding='utf-8') as j:
        data = json.load(j)

    # Пустой список для будущей записи в .txt
    result = []
    # Сохраняем алфавитный порядок
    ord_dict = OrderedDict(data.items())
    # Читаем
    dictionary_reading(ord_dict)
    listed_dictionary = dictionary_to_list(ord_dict, result, prefix='')
    listed_dictionaty_to_txt(listed_dictionary)
    
    

if __name__ == "__main__":
    main('example_dictionary.json')



