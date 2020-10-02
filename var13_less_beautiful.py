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

def_dict = {"A":{"*":[{"Соединяет предложения или члены предложения, выражая противопоставление, сопоставление.":
                                                            ["Он поехал, а я остался.", "Красив, а не умен."]}, 
                    {"Хорошая буква.": ["А так хороша!"]}], 

            "Б": {"*": [{"Две первые буквы алфавита.": ["Знаю а."]}], 
                 "А": {"Ж" : {"У": {"Р": {"*": [{"Колпак для лампы, светильника.": ["Зеленый а."]}]
                                            }
                                    }
                                }
                            },
                 "З": {"А": {"Ц": {"*": [{" Красная строка, отступ в начале строки.": ["Начать писать с абзаца."]}, 
                                        {"Текст между двумя такими отступами. ": ["Прочесть первый а."]}]
                                    }
                             }
                        }
                    }
                },
        "Б": {"А": {"Л": {"*": [{"Большой танцевальный вечер.": ["Костюмированный б."]}], 
                         "Л": {"*": [{"Единица оценки степени, силы какого-н. физического явления (спец.).": 
                                                            ["Ветер в шесть баллов.", "Землетрясение в восемь баллов."]}]
                                }
                            }
                        }
                }
            }

import json
from collections import OrderedDict 
 

# ЧАСТЬ 1. ФУНКЦИЯ ЧТЕНИЯ

def dictionary_reading(current_node, prefix=''):
    """Выводит словарь в читабельном виде"""

    # Перебираем буквы-ключи и их поддеревья
    for letter, value in sorted(current_node.items()):
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
                number += 1
            print("\n")
                
        else:
            # Если не конец слова, добавляем к префиксу следующую букву и 
            # рекурсивно вызываем функцию для следующей вершины.
            dictionary_reading(value, prefix+letter)


# ЧАСТЬ 2. ФУНКЦИЯ ЗАПИСИ
def dictionary_to_txt(current_node, destination, prefix=''):

    with open(destination, "a", encoding="utf-8") as txt:
        od = OrderedDict(sorted(current_node.items()))
        for letter, value in od.items():
            if letter == '*':
                txt.write(prefix + ". ")
                number = 1

                for definitions in value:
                    for definition, examples in definitions.items():
                        if len(value) > 1:
                            txt.write(" " + str(number) + ". " + definition + " Пример(ы): ")
                            pass
                        else:
                            txt.write(definition + " Пример(ы): ")
                            pass
                        for example in examples:
                            txt.write(" " + example)
                            pass
                    number += 1
                txt.write("\n")
                    
            else:
                dictionary_to_txt(value, destination, prefix+letter)


def main(some_json):
    """Пример работы со словарём def_dict"""
    with open(some_json, encoding='utf-8') as j:
        data = json.load(j)
    dict_ = OrderedDict(sorted(data.items()))
    dictionary_reading(dict_)
    dictionary_to_txt(dict_, "dict_file.txt", prefix='')

if __name__ == "__main__":
    main("example_dictionary.json")